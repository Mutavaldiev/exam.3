/* EduNova interactions */
document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-menu]");
  if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
      const open = menu.classList.toggle("is-open");
      menuButton.setAttribute("aria-expanded", String(open));
    });
    menu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
      menu.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
    }));
  }

  // Reveal elements as they enter the viewport.
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
    revealItems.forEach(item => item.classList.add("is-visible"));
  }

  // Client-side course search and category chips.
  const search = document.querySelector("[data-course-search]");
  const cards = [...document.querySelectorAll("[data-course-card]")];
  const filterButtons = [...document.querySelectorAll("[data-filter]")];
  let activeFilter = "all";
  const normalize = value => (value || "").toLowerCase().trim();
  const applyFilters = () => {
    const term = normalize(search?.value);
    cards.forEach(card => {
      const category = normalize(card.dataset.category);
      const text = normalize(card.textContent);
      const categoryMatch = activeFilter === "all" || category.includes(activeFilter);
      const searchMatch = !term || text.includes(term);
      card.classList.toggle("is-hidden", !(categoryMatch && searchMatch));
    });
  };
  search?.addEventListener("input", applyFilters);
  filterButtons.forEach(button => button.addEventListener("click", () => {
    activeFilter = button.dataset.filter || "all";
    filterButtons.forEach(item => item.classList.toggle("is-active", item === button));
    applyFilters();
  }));

  // Add a small confirmation before submitting destructive forms.
  document.querySelectorAll(".button-danger").forEach(button => {
    button.closest("form")?.addEventListener("submit", event => {
      if (!window.confirm("Are you sure you want to continue?")) event.preventDefault();
    });
  });

  // Friendly image fallback if an external or uploaded image is unavailable.
  document.querySelectorAll("img").forEach(img => {
    img.addEventListener("error", () => {
      img.classList.add("image-unavailable");
      img.alt = img.alt || "Image unavailable";
    }, { once: true });
  });
});
