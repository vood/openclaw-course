(function () {
    'use strict';

    var params = new URLSearchParams(window.location.search);
    var moduleId = params.get('module');
    var result = findModule(moduleId);

    if (!result) {
        document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;color:#e8e8ed;font-family:Inter,sans-serif">Module not found</div>';
        return;
    }

    var course = result.course;
    var mod = result.module;

    // Set page title
    document.title = mod.title + ' — OpenClaw Academy';

    // Populate header
    var titleEl = document.getElementById('viewer-title');
    var counterEl = document.getElementById('viewer-counter');
    var progressBar = document.getElementById('viewer-progress-bar');

    if (titleEl) {
        titleEl.textContent = mod.label === mod.title ? mod.title : mod.label + ': ' + mod.title;
    }

    // Load slides iframe
    var iframe = document.getElementById('slides-frame');
    if (iframe) {
        iframe.src = mod.slidesUrl;
    }

    // Forward keyboard navigation to iframe when parent has focus
    document.addEventListener('keydown', function (e) {
        if (!iframe || !iframe.contentWindow) return;
        // Don't forward if user is typing in a form element
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            iframe.contentWindow.postMessage({ type: 'next' }, '*');
        } else if (e.key === 'ArrowLeft' || e.key === 'Backspace') {
            e.preventDefault();
            iframe.contentWindow.postMessage({ type: 'prev' }, '*');
        }
    });

    // Track current slide
    var currentSlide = 1;
    var totalSlides = mod.slideCount;

    // Listen for slide changes from iframe
    window.addEventListener('message', function (e) {
        if (e.data && e.data.type === 'slideChange') {
            currentSlide = e.data.current;
            totalSlides = e.data.total;
            if (counterEl) counterEl.textContent = currentSlide + ' / ' + totalSlides;
            if (progressBar) progressBar.style.width = (currentSlide / totalSlides) * 100 + '%';
            highlightCurrentSection();
        }
    });

    // Module navigation (prev/next session)
    var prevBtn = document.getElementById('prev-module');
    var nextBtn = document.getElementById('next-module');
    var modIndex = course.modules.indexOf(mod);

    if (prevBtn) {
        if (modIndex > 0) {
            prevBtn.href = 'course-viewer.html?module=' + course.modules[modIndex - 1].id;
            prevBtn.title = course.modules[modIndex - 1].title;
        } else {
            prevBtn.style.visibility = 'hidden';
        }
    }
    if (nextBtn) {
        if (modIndex < course.modules.length - 1) {
            nextBtn.href = 'course-viewer.html?module=' + course.modules[modIndex + 1].id;
            nextBtn.title = course.modules[modIndex + 1].title;
        } else {
            nextBtn.style.visibility = 'hidden';
        }
    }

    // Sidebar tabs
    var tocTab = document.getElementById('tab-toc');
    var contentTab = document.getElementById('tab-content');
    var tocPanel = document.getElementById('sidebar-toc');
    var contentPanel = document.getElementById('sidebar-content');

    function switchTab(tab) {
        if (!tocTab || !contentTab) return;
        tocTab.classList.toggle('active', tab === 'toc');
        contentTab.classList.toggle('active', tab === 'content');
        tocPanel.classList.toggle('active', tab === 'toc');
        contentPanel.classList.toggle('active', tab === 'content');
    }

    if (tocTab) tocTab.addEventListener('click', function () { switchTab('toc'); });
    if (contentTab) contentTab.addEventListener('click', function () { switchTab('content'); });

    // Mobile sidebar toggle
    var sidebar = document.querySelector('.viewer-sidebar');
    var toggle = document.querySelector('.sidebar-toggle');
    var overlay = document.querySelector('.sidebar-overlay');

    function toggleSidebar() {
        if (!sidebar) return;
        sidebar.classList.toggle('open');
        if (overlay) overlay.classList.toggle('open');
    }

    if (toggle) toggle.addEventListener('click', toggleSidebar);
    if (overlay) overlay.addEventListener('click', toggleSidebar);

    // Load materials from inlined MATERIALS object or fetch as fallback
    var md = (typeof MATERIALS !== 'undefined' && MATERIALS[moduleId]) ? MATERIALS[moduleId] : null;

    if (!md && !mod.materialUrl) {
        if (tocPanel) {
            tocPanel.innerHTML = '<div class="sidebar-empty">No materials for this session</div>';
            tocPanel.classList.add('active');
        }
        if (contentPanel) {
            contentPanel.innerHTML = '<div class="sidebar-empty">No materials for this session</div>';
        }
        return;
    }

    // Heading-to-slide mapping: sections in the TOC become clickable and jump to slides
    var sectionSlideMap = []; // { headingEl, tocEl, slideIndex }

    function renderMaterials(md) {
        // Strip YAML frontmatter if present
        md = md.replace(/^---[\s\S]*?---\s*/, '');

        var html = marked.parse(md, {
            gfm: true,
            breaks: false
        });

        if (contentPanel) {
            contentPanel.innerHTML = html;
        }

        buildTOC();

        if (window.mermaid && contentPanel && contentPanel.querySelector('.language-mermaid')) {
            contentPanel.querySelectorAll('pre code.language-mermaid').forEach(function (block) {
                var div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = block.textContent;
                block.parentElement.replaceWith(div);
            });
            mermaid.run();
        }

        switchTab('toc');
    }

    if (md) {
        // Use inlined materials (works with file:// protocol)
        renderMaterials(md);
    } else if (mod.materialUrl) {
        // Fallback to fetch (works with http:// server)
        if (contentPanel) contentPanel.innerHTML = '<div class="sidebar-loading">Loading materials...</div>';
        fetch(mod.materialUrl)
            .then(function (res) {
                if (!res.ok) throw new Error('Failed to load');
                return res.text();
            })
            .then(renderMaterials)
            .catch(function () {
                if (contentPanel) contentPanel.innerHTML = '<div class="sidebar-empty">Could not load materials</div>';
                if (tocPanel) {
                    tocPanel.innerHTML = '<div class="sidebar-empty">Could not load materials</div>';
                    tocPanel.classList.add('active');
                }
            });
    }

    function buildTOC() {
        if (!tocPanel || !contentPanel) return;

        var headings = contentPanel.querySelectorAll('h1, h2, h3');
        if (headings.length === 0) {
            tocPanel.innerHTML = '<div class="sidebar-empty">No chapters found</div>';
            tocPanel.classList.add('active');
            return;
        }

        tocPanel.innerHTML = '';
        sectionSlideMap = [];
        var fragment = document.createDocumentFragment();

        // Calculate approximate slide index per heading based on position ratio
        var totalHeadings = headings.length;

        headings.forEach(function (heading, i) {
            var id = 'section-' + i;
            heading.id = id;

            // Approximate which slide this section corresponds to
            // Distribute sections proportionally across slides
            var approxSlide = Math.round((i / totalHeadings) * totalSlides) + 1;

            var link = document.createElement('a');
            link.className = 'toc-item toc-' + heading.tagName.toLowerCase();
            link.textContent = heading.textContent;
            link.href = '#' + id;
            link.setAttribute('data-slide', approxSlide);

            link.addEventListener('click', function (e) {
                e.preventDefault();

                // Navigate slides to this section
                var slideIdx = parseInt(link.getAttribute('data-slide'), 10) - 1;
                if (iframe && iframe.contentWindow) {
                    iframe.contentWindow.postMessage({ type: 'goToSlide', index: slideIdx }, '*');
                }

                // Also scroll the content view
                switchTab('content');
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Update active state
                tocPanel.querySelectorAll('.toc-item').forEach(function (el) { el.classList.remove('active'); });
                link.classList.add('active');
            });

            sectionSlideMap.push({ headingEl: heading, tocEl: link, slideIndex: approxSlide });
            fragment.appendChild(link);
        });

        tocPanel.appendChild(fragment);

        // Track scroll position to highlight active TOC item when in content view
        contentPanel.addEventListener('scroll', debounce(function () {
            var scrollTop = contentPanel.scrollTop;
            var active = null;

            headings.forEach(function (heading) {
                if (heading.offsetTop - 40 <= scrollTop) {
                    active = heading.id;
                }
            });

            tocPanel.querySelectorAll('.toc-item').forEach(function (el) {
                el.classList.toggle('active', el.getAttribute('href') === '#' + active);
            });
        }, 50));
    }

    // When slides change, highlight the corresponding TOC section and scroll content
    function highlightCurrentSection() {
        if (sectionSlideMap.length === 0) return;

        // Find the section whose slide is closest to (but not exceeding) current slide
        var bestMatch = null;
        for (var i = 0; i < sectionSlideMap.length; i++) {
            if (sectionSlideMap[i].slideIndex <= currentSlide) {
                bestMatch = sectionSlideMap[i];
            }
        }

        if (!bestMatch) return;

        // Highlight in TOC
        tocPanel.querySelectorAll('.toc-item').forEach(function (el) { el.classList.remove('active'); });
        bestMatch.tocEl.classList.add('active');

        // Scroll TOC to keep active item visible
        bestMatch.tocEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Scroll content panel to the matching section
        if (contentPanel.classList.contains('active')) {
            bestMatch.headingEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function debounce(fn, ms) {
        var timer;
        return function () {
            clearTimeout(timer);
            timer = setTimeout(fn, ms);
        };
    }
})();
