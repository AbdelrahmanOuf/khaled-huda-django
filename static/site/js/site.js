(() => {
  "use strict";

  const header = document.querySelector("[data-header]");
  const progress = document.querySelector("[data-page-progress]");
  const navToggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const syncScrollUI = () => {
    const y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 30);
    if (progress) {
      const doc = document.documentElement;
      const max = Math.max(1, doc.scrollHeight - window.innerHeight);
      progress.style.width = `${Math.min(100, Math.max(0, (y / max) * 100))}%`;
    }
  };

  syncScrollUI();
  window.addEventListener("scroll", syncScrollUI, { passive: true });
  window.addEventListener("resize", syncScrollUI, { passive: true });

  if (navToggle && nav) {
    const setNav = (open) => {
      nav.classList.toggle("is-open", open);
      navToggle.setAttribute("aria-expanded", String(open));
    };

    navToggle.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setNav(false)));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setNav(false);
    });
    document.addEventListener("click", (event) => {
      if (!nav.contains(event.target) && !navToggle.contains(event.target)) setNav(false);
    });
  }

  const revealItems = [...document.querySelectorAll(".reveal")];
  if ("IntersectionObserver" in window && !reduceMotion) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px" });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  const countdown = document.querySelector("[data-countdown]");
  if (countdown) {
    const target = new Date(countdown.dataset.countdown).getTime();
    if (!Number.isNaN(target)) {
      const fields = {
        days: countdown.querySelector("[data-days]"),
        hours: countdown.querySelector("[data-hours]"),
        minutes: countdown.querySelector("[data-minutes]"),
        seconds: countdown.querySelector("[data-seconds]"),
      };

      const renderCountdown = () => {
        const diff = Math.max(0, target - Date.now());
        const values = {
          days: Math.floor(diff / 86400000),
          hours: Math.floor((diff / 3600000) % 24),
          minutes: Math.floor((diff / 60000) % 60),
          seconds: Math.floor((diff / 1000) % 60),
        };
        Object.entries(values).forEach(([key, value]) => {
          if (fields[key]) fields[key].textContent = String(value).padStart(2, "0");
        });
        return diff > 0;
      };

      renderCountdown();
      const timer = window.setInterval(() => {
        if (!renderCountdown()) window.clearInterval(timer);
      }, 1000);
    }
  }

  if (!reduceMotion) {
    const hero = document.querySelector(".hero");
    const heroContent = document.querySelector(".hero-content");
    const onHeroParallax = () => {
      if (!hero || !heroContent || window.innerWidth < 760) return;
      const rect = hero.getBoundingClientRect();
      if (rect.bottom <= 0 || rect.top >= window.innerHeight) return;
      const offset = Math.min(80, Math.max(0, window.scrollY * 0.08));
      heroContent.style.transform = `translate3d(0, ${offset}px, 0)`;
      heroContent.style.opacity = String(Math.max(0.62, 1 - window.scrollY / 1100));
    };
    onHeroParallax();
    window.addEventListener("scroll", onHeroParallax, { passive: true });
  }
})();
