
/* EduNova interactions */

document.addEventListener("DOMContentLoaded", () => {

  // =====================================
  // NIGHT MODE
  // =====================================
// =================================
// EDUNOVA THEME SWITCH
// =================================

const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeText = document.getElementById("themeText");

function setTheme(theme) {

    document.body.classList.toggle(
        "dark-mode",
        theme === "dark"
    );

    if (themeIcon) {
        themeIcon.textContent =
            theme === "dark" ? "☀" : "☾";
    }

    if (themeText) {
        themeText.textContent =
            theme === "dark" ? "Day mode" : "Night mode";
    }

    if (themeToggle) {
        themeToggle.setAttribute(
            "aria-pressed",
            String(theme === "dark")
        );
    }
}

let currentTheme = "light";

try {
    currentTheme = localStorage.getItem("edunova-theme") || "light";
} catch (error) {}

setTheme(currentTheme);

themeToggle?.addEventListener("click", function () {

    const newTheme =
        document.body.classList.contains("dark-mode")
            ? "light"
            : "dark";

    setTheme(newTheme);

    try {
        localStorage.setItem("edunova-theme", newTheme);
    } catch (error) {}

});

  // =====================================
  // MOBILE MENU
  // =====================================

  const menuButton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-menu]");

  if (menuButton && menu) {

    menuButton.addEventListener("click", () => {

      const open = menu.classList.toggle("is-open");

      menuButton.setAttribute(
        "aria-expanded",
        String(open)
      );

    });

    menu.querySelectorAll("a").forEach(link => {

      link.addEventListener("click", () => {

        menu.classList.remove("is-open");

        menuButton.setAttribute(
          "aria-expanded",
          "false"
        );

      });

    });

  }


  // =====================================
  // REVEAL ANIMATIONS
  // =====================================

  const revealItems = document.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window) {

    const observer = new IntersectionObserver(entries => {

      entries.forEach(entry => {

        if (entry.isIntersecting) {

          entry.target.classList.add("is-visible");

          observer.unobserve(entry.target);

        }

      });

    }, { threshold: 0.12 });

    revealItems.forEach(item => observer.observe(item));

  } else {

    revealItems.forEach(item =>
      item.classList.add("is-visible")
    );

  }


  // =====================================
  // COURSE SEARCH AND FILTERS
  // =====================================

  const search = document.querySelector("[data-course-search]");

  const cards = [
    ...document.querySelectorAll("[data-course-card]")
  ];

  const filterButtons = [
    ...document.querySelectorAll("[data-filter]")
  ];

  let activeFilter = "all";

  const normalize = value =>
    (value || "").toLowerCase().trim();

  const applyFilters = () => {

    const term = normalize(search?.value);

    cards.forEach(card => {

      const category = normalize(card.dataset.category);

      const text = normalize(card.textContent);

      const categoryMatch =
        activeFilter === "all" ||
        category.includes(activeFilter);

      const searchMatch =
        !term || text.includes(term);

      card.classList.toggle(
        "is-hidden",
        !(categoryMatch && searchMatch)
      );

    });

  };

  search?.addEventListener("input", applyFilters);

  filterButtons.forEach(button => {

    button.addEventListener("click", () => {

      activeFilter = button.dataset.filter || "all";

      filterButtons.forEach(item => {

        item.classList.toggle(
          "is-active",
          item === button
        );

      });

      applyFilters();

    });

  });


  // =====================================
  // DELETE CONFIRMATION
  // =====================================

  document.querySelectorAll(".button-danger").forEach(button => {

    button.closest("form")?.addEventListener("submit", event => {

      if (!window.confirm("Are you sure you want to continue?")) {

        event.preventDefault();

      }

    });

  });


  // =====================================
  // IMAGE FALLBACK
  // =====================================

  document.querySelectorAll("img").forEach(img => {

    img.addEventListener("error", () => {

      img.classList.add("image-unavailable");

      img.alt = img.alt || "Image unavailable";

    }, { once: true });

  });

});






/* =========================================
   COURSES — LEFT / RIGHT REVEAL
========================================= */
/* ==========================================
   3D COURSE REVEAL ANIMATION
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    const courses = [
        ...document.querySelectorAll(
            ".course-card, [data-course-card]"
        )
    ];

    if (!courses.length) return;

    const grid = courses[0].parentElement;

    if (grid) {
        grid.classList.add("courses-split-grid");
    }

    // Курсҳоро ба ду самт ҷудо мекунем
    courses.forEach((course, index) => {

        course.classList.remove(
            "split-left",
            "split-right",
            "split-visible"
        );

        if (index % 2 === 0) {
            course.classList.add("split-left");
        } else {
            course.classList.add("split-right");
        }

        course.style.transitionDelay =
            `${(index % 2) * 150}ms`;

    });

    // Ҳангоми ба экран даромадан аниматсия иҷро мешавад
    const observer = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add(
                        "split-visible"
                    );

                    // Як маротиба иҷро мешавад
                    observer.unobserve(entry.target);
                }

            });

        },
        {
            threshold: 0.15
        }
    );

    courses.forEach(course => {
        observer.observe(course);
    });

});