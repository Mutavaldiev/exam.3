
/* ==========================================
   EDUNOVA 2.0 — PREMIUM INTERACTIONS
   Frontend only: HTML + CSS + JavaScript
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    "use strict";

    /* ======================================
       1. SELECT ELEMENTS
    ====================================== */

    const body = document.body;
    const header = document.getElementById("siteHeader");
    const menuToggle = document.getElementById("menuToggle");
    const menu = document.getElementById("mainMenu");

    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");
    const themeText = document.getElementById("themeText");

    const scrollProgress = document.getElementById("scrollProgress");
    const backToTop = document.getElementById("backToTop");


    /* ======================================
       2. THEME SYSTEM
    ====================================== */

    function getSavedTheme() {
        try {
            return localStorage.getItem("edunova-theme") || "light";
        } catch (error) {
            return "light";
        }
    }

    function setTheme(theme) {

        const dark = theme === "dark";

        body.classList.toggle("dark-mode", dark);

        if (themeIcon) {
            themeIcon.className = dark
                ? "fa-solid fa-sun"
                : "fa-solid fa-moon";
        }

        if (themeText) {
            themeText.textContent = dark
                ? "Light mode"
                : "Dark mode";
        }

        if (themeToggle) {
            themeToggle.setAttribute(
                "aria-pressed",
                String(dark)
            );
        }

        try {
            localStorage.setItem("edunova-theme", theme);
        } catch (error) {
            // Theme still works without localStorage.
        }
    }

    setTheme(getSavedTheme());

    themeToggle?.addEventListener("click", () => {

        const newTheme = body.classList.contains("dark-mode")
            ? "light"
            : "dark";

        setTheme(newTheme);

    });


    /* ======================================
       3. MOBILE NAVIGATION
    ====================================== */

    function closeMenu() {

        if (!menu || !menuToggle) return;

        menu.classList.remove("is-open");

        menuToggle.classList.remove("active");

        menuToggle.setAttribute("aria-expanded", "false");

    }

    menuToggle?.addEventListener("click", () => {

        const opened = menu?.classList.toggle("is-open");

        menuToggle.classList.toggle("active", Boolean(opened));

        menuToggle.setAttribute(
            "aria-expanded",
            String(Boolean(opened))
        );

    });

    menu?.querySelectorAll("a").forEach(link => {

        link.addEventListener("click", closeMenu);

    });

    document.addEventListener("click", event => {

        if (
            menu &&
            menuToggle &&
            !menu.contains(event.target) &&
            !menuToggle.contains(event.target)
        ) {
            closeMenu();
        }

    });

    window.addEventListener("resize", () => {

        if (window.innerWidth > 700) {
            closeMenu();
        }

    });


    /* ======================================
       4. SCROLL EFFECTS
    ====================================== */

    let scrollScheduled = false;

    function updateScrollEffects() {

        const scrollTop = window.scrollY;

        const pageHeight =
            document.documentElement.scrollHeight -
            window.innerHeight;

        const progress = pageHeight > 0
            ? (scrollTop / pageHeight) * 100
            : 0;

        if (scrollProgress) {
            scrollProgress.style.width = `${progress}%`;
        }

        header?.classList.toggle(
            "header-scrolled",
            scrollTop > 30
        );

        backToTop?.classList.toggle(
            "show",
            scrollTop > 450
        );

        scrollScheduled = false;

    }

    window.addEventListener("scroll", () => {

        if (!scrollScheduled) {

            requestAnimationFrame(updateScrollEffects);

            scrollScheduled = true;

        }

    }, { passive: true });

    updateScrollEffects();

    backToTop?.addEventListener("click", () => {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });


    /* ======================================
       5. REVEAL ANIMATIONS
    ====================================== */

    const revealElements = document.querySelectorAll(
        ".reveal, .course-card, .dashboard-tile, " +
        ".content-card, .section-heading, .stats-strip"
    );

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if ("IntersectionObserver" in window && !reduceMotion) {

        const revealObserver = new IntersectionObserver(
            (entries, observer) => {

                entries.forEach(entry => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add("is-visible");

                        observer.unobserve(entry.target);

                    }

                });

            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -40px 0px"
            }
        );

        revealElements.forEach((element, index) => {

            element.style.transitionDelay =
                `${Math.min(index % 5, 4) * 80}ms`;

            revealObserver.observe(element);

        });

    } else {

        revealElements.forEach(element => {
            element.classList.add("is-visible");
        });

    }


    /* ======================================
       6. COURSE SEARCH AND FILTER
    ====================================== */

    const searchInput = document.querySelector(
        "[data-course-search]"
    );

    const courseCards = [
        ...document.querySelectorAll("[data-course-card]")
    ];

    const filterButtons = [
        ...document.querySelectorAll("[data-filter]")
    ];

    let activeFilter = "all";

    function normalizeText(value) {

        return String(value || "")
            .toLowerCase()
            .trim();

    }

    function filterCourses() {

        const searchTerm = normalizeText(searchInput?.value);

        let visibleCount = 0;

        courseCards.forEach(card => {

            const category = normalizeText(
                card.dataset.category
            );

            const cardText = normalizeText(
                card.textContent
            );

            const matchesCategory =
                activeFilter === "all" ||
                category.includes(activeFilter);

            const matchesSearch =
                !searchTerm ||
                cardText.includes(searchTerm);

            const visible =
                matchesCategory && matchesSearch;

            card.classList.toggle("is-hidden", !visible);

            if (visible) {
                visibleCount++;
            }

        });

        const emptyState = document.querySelector(
            "[data-empty-state]"
        );

        if (emptyState) {
            emptyState.hidden = visibleCount !== 0;
        }

    }

    searchInput?.addEventListener("input", filterCourses);

    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            activeFilter = normalizeText(
                button.dataset.filter || "all"
            );

            filterButtons.forEach(item => {

                const active = item === button;

                item.classList.toggle("is-active", active);

                item.setAttribute(
                    "aria-pressed",
                    String(active)
                );

            });

            filterCourses();

        });

    });


    /* ======================================
       7. 3D COURSE CARD EFFECT
    ====================================== */

    const cards3D = document.querySelectorAll(
        ".course-card, .dashboard-tile"
    );

    if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {

        cards3D.forEach(card => {

            card.addEventListener("pointermove", event => {

                const rect = card.getBoundingClientRect();

                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((centerY - y) / centerY) * 3;
                const rotateY = ((x - centerX) / centerX) * 3;

                card.style.transform =
                    `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;

            });

            card.addEventListener("pointerleave", () => {

                card.style.transform = "";

            });

        });

    }


    /* ======================================
       8. BUTTON RIPPLE EFFECT
    ====================================== */

    document.querySelectorAll(
        ".button, .chip, .theme-switch"
    ).forEach(button => {

        button.addEventListener("click", event => {

            if (reduceMotion) return;

            const rect = button.getBoundingClientRect();

            const ripple = document.createElement("span");

            ripple.className = "button-ripple";

            ripple.style.left =
                `${event.clientX - rect.left}px`;

            ripple.style.top =
                `${event.clientY - rect.top}px`;

            button.appendChild(ripple);

            ripple.addEventListener("animationend", () => {
                ripple.remove();
            }, { once: true });

        });

    });


    /* ======================================
       9. IMAGE ERROR HANDLING
    ====================================== */

    document.querySelectorAll("img").forEach(img => {

        img.addEventListener("error", () => {

            img.classList.add("image-unavailable");

            img.alt = img.alt || "Image unavailable";

        }, { once: true });

    });


    /* ======================================
       10. DELETE CONFIRMATION
    ====================================== */

    document.querySelectorAll(
        "form button.button-danger"
    ).forEach(button => {

        const form = button.closest("form");

        form?.addEventListener("submit", event => {

            const confirmed = window.confirm(
                "Are you sure you want to continue?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    /* ======================================
       11. ACTIVE NAVIGATION
    ====================================== */

    const currentPath = window.location.pathname;

    document.querySelectorAll(
        ".main-nav a"
    ).forEach(link => {

        const linkPath = new URL(
            link.href,
            window.location.origin
        ).pathname;

        if (
            linkPath === currentPath &&
            currentPath !== "/"
        ) {

            link.classList.add("active");

            link.setAttribute("aria-current", "page");

        }

    });


    /* ======================================
       12. COUNTER ANIMATION
    ====================================== */

    const counters = document.querySelectorAll(
        "[data-counter]"
    );

    function animateCounter(element) {

        const target = Number(element.dataset.counter);

        if (!Number.isFinite(target)) return;

        const duration = 1400;
        const startTime = performance.now();

        function update(now) {

            const progress = Math.min(
                (now - startTime) / duration,
                1
            );

            const eased =
                1 - Math.pow(1 - progress, 4);

            const current = Math.floor(
                target * eased
            );

            element.textContent =
                current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent =
                    target.toLocaleString();
            }

        }

        requestAnimationFrame(update);

    }

    if ("IntersectionObserver" in window && !reduceMotion) {

        const counterObserver = new IntersectionObserver(
            (entries, observer) => {

                entries.forEach(entry => {

                    if (entry.isIntersecting) {

                        animateCounter(entry.target);

                        observer.unobserve(entry.target);

                    }

                });

            },
            { threshold: 0.5 }
        );

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });

    } else {

        counters.forEach(counter => {
            counter.textContent =
                Number(counter.dataset.counter).toLocaleString();
        });

    }


    /* ======================================
       13. SMOOTH ANCHOR NAVIGATION
    ====================================== */

    document.querySelectorAll(
        'a[href^="#"]'
    ).forEach(link => {

        link.addEventListener("click", event => {

            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") return;

            const target = document.querySelector(targetId);

            if (!target) return;

            event.preventDefault();

            target.scrollIntoView({
                behavior: reduceMotion ? "auto" : "smooth",
                block: "start"
            });

        });

    });


    /* ======================================
       14. KEYBOARD ACCESSIBILITY
    ====================================== */

    document.addEventListener("keydown", event => {

        if (event.key === "Escape") {
            closeMenu();
        }

    });


    /* ======================================
       15. PAGE READY
    ====================================== */

    body.classList.add("page-loaded");

    console.log(
        "%c EduNova 2.0 ",
        "background:#7557f5;color:white;padding:10px 18px;border-radius:8px;font-weight:bold;"
    );

    console.log(
        "Welcome to EduNova — Learn Without Limits!"
    );

});
