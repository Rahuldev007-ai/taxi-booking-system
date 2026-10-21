/**
 * CabZy — Real-Time Map & Auto-Suggestions Engine
 * Powered by Leaflet, Esri WorldStreetMap, Photon by Komoot, Nominatim & OSRM
 * 100% Free - Zero API Keys Required - Zero Watermarks - Never Blocked
 */

(function () {
    'use strict';

    let map = null;
    let markersLayer = null;
    let routeLayer = null;
    let pickupMarker = null;
    let destMarker = null;

    let sourceCoords = null; // { lat, lng, name }
    let destCoords = null;   // { lat, lng, name }

    let sourceAbortCtrl = null;
    let destAbortCtrl = null;

    // Default map center (Mumbai Metropolitan Area)
    const DEFAULT_LAT = 19.0760;
    const DEFAULT_LNG = 72.8777;
    const DEFAULT_ZOOM = 12;

    /**
     * Debounce helper
     */
    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    /**
     * Deduplicate and clean address string components with correct comma spacing
     */
    function cleanAddressParts(parts) {
        const seen = new Set();
        const cleaned = [];

        for (let pt of parts) {
            if (!pt) continue;
            const subParts = pt.split(',').map(s => s.trim()).filter(Boolean);
            for (const sp of subParts) {
                const lower = sp.toLowerCase();
                if (!seen.has(lower)) {
                    seen.add(lower);
                    cleaned.push(sp);
                }
            }
        }
        return cleaned;
    }

    /**
     * Format a geocoding item (from Photon or Nominatim) with proper spacing
     */
    function formatGeocodedItem(item) {
        if (item.properties) {
            // Photon GeoJSON format
            const p = item.properties;
            const parts = [];
            if (p.name) parts.push(p.name);
            const locality = p.district || p.locality || p.suburb || p.street || '';
            if (locality) parts.push(locality);
            const city = p.city || p.county || '';
            if (city) parts.push(city);
            const state = p.state || '';
            if (state) parts.push(state);
            const country = p.country || '';
            if (country) parts.push(country);

            const cleaned = cleanAddressParts(parts);
            const primary = p.name || cleaned[0] || 'Selected Location';
            const secondary = cleaned.slice(1).join(', ') || p.country || '';
            const fullText = cleaned.join(', ');

            return {
                primary: primary,
                secondary: secondary,
                fullText: fullText,
                lat: item.geometry.coordinates[1],
                lng: item.geometry.coordinates[0]
            };
        } else {
            // Nominatim JSON format
            const rawName = item.name || (item.display_name ? item.display_name.split(',')[0].trim() : 'Location');
            const allParts = cleanAddressParts((item.display_name || '').split(','));
            const primary = rawName;
            const secondary = allParts.filter(p => p.toLowerCase() !== primary.toLowerCase()).join(', ');
            const fullText = allParts.join(', ');

            return {
                primary: primary,
                secondary: secondary,
                fullText: fullText,
                lat: parseFloat(item.lat),
                lng: parseFloat(item.lon)
            };
        }
    }

    /**
     * Fetch auto-suggestions using Photon API with location bias, and fallback to Nominatim
     */
    async function fetchSuggestions(query, abortCtrl) {
        if (!query || query.trim().length < 2) return [];

        const cleanQuery = query.trim();
        // Location bias: anchor near current pickup coordinates or default region
        const biasLat = sourceCoords ? sourceCoords.lat : DEFAULT_LAT;
        const biasLng = sourceCoords ? sourceCoords.lng : DEFAULT_LNG;

        // Photon with geographical bias
        const photonUrl = `https://photon.komoot.io/api/?q=${encodeURIComponent(cleanQuery)}&lat=${biasLat}&lon=${biasLng}&limit=6`;

        try {
            const resp = await fetch(photonUrl, { signal: abortCtrl.signal });
            if (resp.ok) {
                const data = await resp.json();
                if (data && data.features && data.features.length > 0) {
                    return data.features.map(formatGeocodedItem);
                }
            }
        } catch (err) {
            if (err.name === 'AbortError') throw err;
            console.warn('Photon query fallback triggered:', err);
        }

        // Fallback: OpenStreetMap Nominatim with India bias
        const nominatimUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(cleanQuery)}&limit=6&addressdetails=1&countrycodes=in`;
        try {
            const resp2 = await fetch(nominatimUrl, {
                signal: abortCtrl.signal,
                headers: { 'Accept-Language': 'en' }
            });
            if (resp2.ok) {
                const data2 = await resp2.json();
                if (Array.isArray(data2) && data2.length > 0) {
                    return data2.map(formatGeocodedItem);
                }
            }
        } catch (err2) {
            if (err2.name === 'AbortError') throw err2;
            console.warn('Nominatim query error:', err2);
        }

        return [];
    }

    /**
     * Reverse Geocode Lat/Lng into clean readable address using Nominatim
     */
    async function reverseGeocode(lat, lng) {
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`;
        try {
            const resp = await fetch(url, { headers: { 'Accept-Language': 'en' } });
            if (resp.ok) {
                const data = await resp.json();
                const formatted = formatGeocodedItem(data);
                return formatted.fullText;
            }
        } catch (err) {
            console.warn('Reverse geocoding error:', err);
        }
        return `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
    }

    /**
     * Create Custom HTML Marker Pins
     */
    function createCustomPin(type) {
        const isPickup = type === 'pickup';
        const className = isPickup ? 'nest-marker-pin nest-marker-pickup' : 'nest-marker-pin nest-marker-dest';
        const iconHtml = isPickup ? '<i class="bi bi-geo-alt-fill"></i>' : '<i class="bi bi-pin-map-fill"></i>';

        return L.divIcon({
            className: 'nest-custom-div-icon',
            html: `<div class="${className}">${iconHtml}</div>`,
            iconSize: [34, 34],
            iconAnchor: [17, 34],
            popupAnchor: [0, -32]
        });
    }

    /**
     * Calculate route via OSRM demo routing engine with straight-line fallback
     */
    async function calculateRoute() {
        if (!sourceCoords || !destCoords || !map) return;

        const statPill = document.getElementById('routeStatPill');
        const statText = document.getElementById('routeStatText');

        if (statPill) {
            statPill.style.display = 'inline-flex';
            if (statText) statText.textContent = 'Calculating optimal driving route...';
        }

        const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${sourceCoords.lng},${sourceCoords.lat};${destCoords.lng},${destCoords.lat}?overview=full&geometries=geojson`;

        try {
            const resp = await fetch(osrmUrl);
            if (resp.ok) {
                const data = await resp.json();
                if (data && data.routes && data.routes.length > 0) {
                    const route = data.routes[0];
                    const distKm = (route.distance / 1000).toFixed(1);
                    const durMins = Math.max(1, Math.round(route.duration / 60));

                    renderRoutePolyline(route.geometry);

                    if (statText) {
                        statText.innerHTML = `<strong>${distKm} km</strong> &bull; ~${durMins} mins drive`;
                    }
                    return;
                }
            }
        } catch (err) {
            console.warn('OSRM routing fallback to geodesic line:', err);
        }

        // Fallback: Haversine distance and direct polyline
        const latlngs = [
            [sourceCoords.lat, sourceCoords.lng],
            [destCoords.lat, destCoords.lng]
        ];
        renderStraightRoute(latlngs);

        const directKm = calculateHaversine(sourceCoords.lat, sourceCoords.lng, destCoords.lat, destCoords.lng).toFixed(1);
        const estMins = Math.max(2, Math.round(directKm * 2.2));
        if (statText) {
            statText.innerHTML = `<strong>~${directKm} km</strong> &bull; ~${estMins} mins direct route`;
        }
    }

    /**
     * Render detailed GeoJSON route polyline
     */
    function renderRoutePolyline(geojsonGeometry) {
        if (!routeLayer || !map) return;
        routeLayer.clearLayers();

        // 1. Shadow / Glow outline
        L.geoJSON(geojsonGeometry, {
            style: {
                color: '#003A40',
                weight: 7,
                opacity: 0.35,
                lineCap: 'round',
                lineJoin: 'round'
            }
        }).addTo(routeLayer);

        // 2. High-contrast route line
        const mainLine = L.geoJSON(geojsonGeometry, {
            style: {
                color: '#D96B43',
                weight: 4.5,
                opacity: 0.95,
                lineCap: 'round',
                lineJoin: 'round'
            }
        }).addTo(routeLayer);

        map.fitBounds(mainLine.getBounds(), {
            padding: [40, 40],
            maxZoom: 16,
            animate: true
        });
    }

    /**
     * Fallback straight polyline
     */
    function renderStraightRoute(latlngs) {
        if (!routeLayer || !map) return;
        routeLayer.clearLayers();

        const poly = L.polyline(latlngs, {
            color: '#D96B43',
            weight: 4,
            opacity: 0.85,
            dashArray: '8, 8'
        }).addTo(routeLayer);

        map.fitBounds(poly.getBounds(), {
            padding: [40, 40],
            maxZoom: 16,
            animate: true
        });
    }

    /**
     * Haversine direct distance formula
     */
    function calculateHaversine(lat1, lon1, lat2, lon2) {
        const R = 6371; // Earth radius km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    /**
     * Update Pickup Marker on Map
     */
    function updatePickupMarker(coords, label) {
        if (!map || !markersLayer) return;
        sourceCoords = { ...coords, name: label };

        if (!pickupMarker) {
            pickupMarker = L.marker([coords.lat, coords.lng], {
                icon: createCustomPin('pickup'),
                draggable: true,
                title: 'Pickup Location (Drag to adjust)'
            }).addTo(markersLayer);

            pickupMarker.on('dragend', async function (e) {
                const pos = e.target.getLatLng();
                sourceCoords = { lat: pos.lat, lng: pos.lng, name: 'Custom Pickup' };
                const address = await reverseGeocode(pos.lat, pos.lng);
                const input = document.getElementById('search_source');
                if (input) input.value = address;
                pickupMarker.bindPopup(`<strong>📍 Pickup:</strong><br>${address}`).openPopup();
                calculateRoute();
            });
        } else {
            pickupMarker.setLatLng([coords.lat, coords.lng]);
        }

        pickupMarker.bindPopup(`<strong>📍 Pickup Location:</strong><br>${label}`).openPopup();

        if (!destCoords) {
            map.flyTo([coords.lat, coords.lng], 14, { duration: 0.8 });
        } else {
            calculateRoute();
        }
    }

    /**
     * Update Destination Marker on Map
     */
    function updateDestMarker(coords, label) {
        if (!map || !markersLayer) return;
        destCoords = { ...coords, name: label };

        if (!destMarker) {
            destMarker = L.marker([coords.lat, coords.lng], {
                icon: createCustomPin('dest'),
                draggable: true,
                title: 'Destination (Drag to adjust)'
            }).addTo(markersLayer);

            destMarker.on('dragend', async function (e) {
                const pos = e.target.getLatLng();
                destCoords = { lat: pos.lat, lng: pos.lng, name: 'Custom Destination' };
                const address = await reverseGeocode(pos.lat, pos.lng);
                const input = document.getElementById('search_destination');
                if (input) input.value = address;
                destMarker.bindPopup(`<strong>🏁 Destination:</strong><br>${address}`).openPopup();
                calculateRoute();
            });
        } else {
            destMarker.setLatLng([coords.lat, coords.lng]);
        }

        destMarker.bindPopup(`<strong>🏁 Destination Point:</strong><br>${label}`).openPopup();

        if (!sourceCoords) {
            map.flyTo([coords.lat, coords.lng], 14, { duration: 0.8 });
        } else {
            calculateRoute();
        }
    }

    /**
     * Setup Autocomplete Dropdown logic for an input field
     */
    function setupAutocomplete(inputId, dropdownId, type) {
        const input = document.getElementById(inputId);
        const dropdown = document.getElementById(dropdownId);
        if (!input || !dropdown) return;

        let activeIndex = -1;

        function closeDropdown() {
            dropdown.style.display = 'none';
            dropdown.innerHTML = '';
            activeIndex = -1;
        }

        function renderSuggestions(items) {
            dropdown.innerHTML = '';
            activeIndex = -1;

            if (items.length === 0) {
                dropdown.innerHTML = '<div class="map-suggestion-empty"><i class="bi bi-info-circle me-1"></i> No matching locations found. Try a different landmark or area.</div>';
                dropdown.style.display = 'block';
                return;
            }

            const iconClass = type === 'pickup' ? 'suggestion-icon-pickup' : 'suggestion-icon-dest';
            const iconSymbol = type === 'pickup' ? 'bi-geo-alt-fill' : 'bi-pin-map-fill';

            items.forEach((item, idx) => {
                const el = document.createElement('div');
                el.className = 'map-suggestion-item';
                el.dataset.index = idx;

                el.innerHTML = `
                    <div class="suggestion-icon ${iconClass}">
                        <i class="bi ${iconSymbol}"></i>
                    </div>
                    <div class="suggestion-content">
                        <div class="suggestion-title">${escapeHtml(item.primary)}</div>
                        <div class="suggestion-subtitle">${escapeHtml(item.secondary || item.fullText)}</div>
                    </div>
                `;

                el.addEventListener('click', () => {
                    selectSuggestion(item);
                });

                dropdown.appendChild(el);
            });

            dropdown.style.display = 'block';
        }

        function selectSuggestion(item) {
            input.value = item.fullText;
            closeDropdown();

            if (type === 'pickup') {
                updatePickupMarker({ lat: item.lat, lng: item.lng }, item.fullText);
            } else {
                updateDestMarker({ lat: item.lat, lng: item.lng }, item.fullText);
            }
        }

        const handleInput = debounce(async function () {
            const val = input.value.trim();
            if (val.length < 2) {
                closeDropdown();
                return;
            }

            // Abort prior fetch
            if (type === 'pickup') {
                if (sourceAbortCtrl) sourceAbortCtrl.abort();
                sourceAbortCtrl = new AbortController();
            } else {
                if (destAbortCtrl) destAbortCtrl.abort();
                destAbortCtrl = new AbortController();
            }
            const activeCtrl = type === 'pickup' ? sourceAbortCtrl : destAbortCtrl;

            dropdown.innerHTML = '<div class="map-suggestion-loading"><div class="spinner-border spinner-border-sm text-secondary me-2" role="status"></div>Searching locations in real-time...</div>';
            dropdown.style.display = 'block';

            try {
                const items = await fetchSuggestions(val, activeCtrl);
                renderSuggestions(items);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    dropdown.innerHTML = '<div class="map-suggestion-empty text-danger"><i class="bi bi-exclamation-circle me-1"></i> Error loading suggestions.</div>';
                }
            }
        }, 280);

        input.addEventListener('input', handleInput);
        input.addEventListener('focus', function () {
            if (input.value.trim().length >= 2 && dropdown.children.length > 0) {
                dropdown.style.display = 'block';
            }
        });

        // Keyboard navigation
        input.addEventListener('keydown', function (e) {
            const items = dropdown.querySelectorAll('.map-suggestion-item');
            if (!items.length || dropdown.style.display === 'none') return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                activeIndex = (activeIndex + 1) % items.length;
                highlightItem(items, activeIndex);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                activeIndex = (activeIndex - 1 + items.length) % items.length;
                highlightItem(items, activeIndex);
            } else if (e.key === 'Enter') {
                if (activeIndex > -1 && items[activeIndex]) {
                    e.preventDefault();
                    items[activeIndex].click();
                }
            } else if (e.key === 'Escape') {
                closeDropdown();
            }
        });

        function highlightItem(items, idx) {
            items.forEach((item, i) => {
                item.classList.toggle('active', i === idx);
                if (i === idx) {
                    item.scrollIntoView({ block: 'nearest' });
                }
            });
        }

        // Close on clicking outside
        document.addEventListener('click', function (e) {
            if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                closeDropdown();
            }
        });
    }

    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Browser Geolocation: Locate User & Reverse-geocode
     */
    function setupGeolocation() {
        const locateBtn = document.getElementById('btnLocateMe');
        const sourceInput = document.getElementById('search_source');
        if (!locateBtn || !sourceInput) return;

        locateBtn.addEventListener('click', function () {
            if (!navigator.geolocation) {
                alert('Geolocation is not supported by your current browser.');
                return;
            }

            locateBtn.disabled = true;
            locateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span>';

            navigator.geolocation.getCurrentPosition(
                async function (pos) {
                    const lat = pos.coords.latitude;
                    const lng = pos.coords.longitude;
                    const address = await reverseGeocode(lat, lng);

                    sourceInput.value = address;
                    updatePickupMarker({ lat, lng }, address);

                    locateBtn.disabled = false;
                    locateBtn.innerHTML = '<i class="bi bi-crosshair text-success"></i>';
                },
                function (err) {
                    locateBtn.disabled = false;
                    locateBtn.innerHTML = '<i class="bi bi-crosshair"></i>';
                    console.warn('Geolocation error:', err);
                    alert('Unable to retrieve your current location. Please verify location permissions.');
                },
                { enableHighAccuracy: true, timeout: 8000 }
            );
        });
    }

    /**
     * Swap Route button (exchanges source & destination)
     */
    function setupRouteSwap() {
        const swapBtn = document.getElementById('swapLocationsBtn');
        const sourceInput = document.getElementById('search_source');
        const destInput = document.getElementById('search_destination');
        if (!swapBtn || !sourceInput || !destInput) return;

        swapBtn.addEventListener('click', function () {
            const tempVal = sourceInput.value;
            sourceInput.value = destInput.value;
            destInput.value = tempVal;

            const tempCoords = sourceCoords;
            sourceCoords = destCoords;
            destCoords = tempCoords;

            if (sourceCoords) {
                updatePickupMarker(sourceCoords, sourceInput.value);
            } else if (pickupMarker) {
                markersLayer.removeLayer(pickupMarker);
                pickupMarker = null;
            }

            if (destCoords) {
                updateDestMarker(destCoords, destInput.value);
            } else if (destMarker) {
                markersLayer.removeLayer(destMarker);
                destMarker = null;
            }

            if (sourceCoords && destCoords) {
                calculateRoute();
            } else if (routeLayer) {
                routeLayer.clearLayers();
                const statPill = document.getElementById('routeStatPill');
                if (statPill) statPill.style.display = 'none';
            }
        });
    }

    /**
     * Popular Quick Pick Destination Chips
     */
    function setupQuickChips() {
        const chips = document.querySelectorAll('.quick-pick-chip');
        const destInput = document.getElementById('search_destination');
        if (!chips.length || !destInput) return;

        chips.forEach(chip => {
            chip.addEventListener('click', async function () {
                const targetText = this.dataset.query || this.textContent.trim();
                destInput.value = targetText;

                // Geocode quickly via Photon with proximity bias
                try {
                    const abortCtrl = new AbortController();
                    const results = await fetchSuggestions(targetText, abortCtrl);
                    if (results.length > 0) {
                        const top = results[0];
                        destInput.value = top.fullText;
                        updateDestMarker({ lat: top.lat, lng: top.lng }, top.fullText);
                    }
                } catch (e) {
                    console.warn('Quick chip geocoding error:', e);
                }
            });
        });
    }

    /**
     * Toggle Map Height (Expand / Compact)
     */
    function setupMapSizeToggle() {
        const toggleBtn = document.getElementById('toggleMapSizeBtn');
        const mapEl = document.getElementById('routeMap');
        if (!toggleBtn || !mapEl) return;

        toggleBtn.addEventListener('click', function () {
            const isExpanded = mapEl.classList.toggle('expanded');
            toggleBtn.innerHTML = isExpanded ? '<i class="bi bi-arrows-angle-contract"></i>' : '<i class="bi bi-arrows-angle-expand"></i>';
            toggleBtn.title = isExpanded ? 'Collapse Map' : 'Expand Map';

            setTimeout(() => {
                if (map) map.invalidateSize();
            }, 320);
        });
    }

    /**
     * Reset Map View Button
     */
    function setupResetView() {
        const resetBtn = document.getElementById('resetMapBtn');
        if (!resetBtn) return;

        resetBtn.addEventListener('click', function () {
            if (!map) return;
            if (sourceCoords && destCoords && routeLayer && routeLayer.getLayers().length > 0) {
                map.fitBounds(routeLayer.getBounds(), { padding: [35, 35] });
            } else if (sourceCoords) {
                map.flyTo([sourceCoords.lat, sourceCoords.lng], 14);
            } else {
                map.flyTo([DEFAULT_LAT, DEFAULT_LNG], DEFAULT_ZOOM);
            }
        });
    }

    /**
     * Click anywhere on Map to pick Source or Destination
     */
    function setupMapClickHandler() {
        if (!map) return;

        map.on('click', async function (e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            const sourceInput = document.getElementById('search_source');
            const destInput = document.getElementById('search_destination');

            if (!sourceInput || !destInput) return;

            const address = await reverseGeocode(lat, lng);

            if (!sourceInput.value.trim()) {
                sourceInput.value = address;
                updatePickupMarker({ lat, lng }, address);
            } else {
                destInput.value = address;
                updateDestMarker({ lat, lng }, address);
            }
        });
    }

    /**
     * Geocode pre-filled inputs on page load (e.g. from previous GET search)
     * Sequenced so destination uses pickup's geographic bias!
     */
    async function geocodeInitialValues() {
        const sourceInput = document.getElementById('search_source');
        const destInput = document.getElementById('search_destination');

        if (sourceInput && sourceInput.value.trim()) {
            try {
                const sRes = await fetchSuggestions(sourceInput.value.trim(), new AbortController());
                if (sRes.length > 0) {
                    const top = sRes[0];
                    updatePickupMarker({ lat: top.lat, lng: top.lng }, sourceInput.value);
                }
            } catch (err) { }
        }

        if (destInput && destInput.value.trim()) {
            try {
                const dRes = await fetchSuggestions(destInput.value.trim(), new AbortController());
                if (dRes.length > 0) {
                    const top = dRes[0];
                    updateDestMarker({ lat: top.lat, lng: top.lng }, destInput.value);
                }
            } catch (err) { }
        }
    }

    /**
     * Initialize Leaflet with 100% Free CARTO Voyager Tiles (OpenStreetMap Data)
     * Solves OSM volunteer server 403 policy blocking completely
     */
    function initMap() {
        const mapContainer = document.getElementById('routeMap');
        if (!mapContainer) return;

        if (typeof L === 'undefined') {
            console.warn('Leaflet library is loading...');
            setTimeout(initMap, 150);
            return;
        }

        // Initialize Leaflet Map
        map = L.map('routeMap', {
            center: [DEFAULT_LAT, DEFAULT_LNG],
            zoom: DEFAULT_ZOOM,
            zoomControl: false // custom placement
        });

        // Add custom zoom control in bottom-right to not overlap stats pill
        L.control.zoom({ position: 'bottomright' }).addTo(map);

        // Esri WorldStreetMap (100% Free, High Resolution, Zero API Key Required, No Watermarks)
        const primaryTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: 'Tiles &copy; <a href="https://www.esri.com" target="_blank" rel="noopener">Esri</a> &mdash; StreetMap',
            referrerPolicy: 'no-referrer'
        }).addTo(map);

        // Fallback tile layer if needed
        primaryTileLayer.on('tileerror', function () {
            console.warn('Esri tile error detected, switching to fallback');
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                referrerPolicy: 'no-referrer',
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
        });

        markersLayer = L.layerGroup().addTo(map);
        routeLayer = L.layerGroup().addTo(map);

        // Bind interactive features
        setupAutocomplete('search_source', 'sourceSuggestions', 'pickup');
        setupAutocomplete('search_destination', 'destSuggestions', 'dest');
        setupGeolocation();
        setupRouteSwap();
        setupQuickChips();
        setupMapSizeToggle();
        setupResetView();
        setupMapClickHandler();

        // Geocode initial values if present
        geocodeInitialValues();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMap);
    } else {
        initMap();
    }
})();
