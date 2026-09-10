(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const intro = document.querySelector("[data-cinematic-intro]");
  const introSkip = document.querySelector("[data-intro-skip]");

  if (intro) {
    const storageKey = "abdelrahmanOmniaIntroSeen";
    const dismissIntro = () => {
      intro.classList.add("is-hidden");
      document.body.classList.remove("intro-active");
      intro.setAttribute("aria-hidden", "true");
      try {
        sessionStorage.setItem(storageKey, "1");
      } catch (_) {
        // sessionStorage can be unavailable in strict privacy modes.
      }
      window.setTimeout(() => intro.remove(), reduceMotion ? 0 : 850);
    };

    let seen = false;
    try {
      seen = sessionStorage.getItem(storageKey) === "1";
    } catch (_) {
      seen = false;
    }

    if (seen || reduceMotion) {
      dismissIntro();
    } else {
      document.body.classList.add("intro-active");
      intro.setAttribute("aria-hidden", "false");
      const timer = window.setTimeout(dismissIntro, 2800);
      if (introSkip) {
        introSkip.addEventListener("click", () => {
          window.clearTimeout(timer);
          dismissIntro();
        }, { once: true });
      }
    }
  }

  const audio = document.querySelector("[data-background-music]");
  const musicToggle = document.querySelector("[data-music-toggle]");
  const musicDock = document.querySelector("[data-music-dock]");
  const musicStatus = document.querySelector("[data-music-status]");

  if (audio && musicToggle) {
    audio.volume = 0.55;

    const syncMusicUI = () => {
      const playing = !audio.paused && !audio.ended;
      musicToggle.setAttribute("aria-pressed", String(playing));
      musicToggle.setAttribute("aria-label", playing ? "Pause background music" : "Play background music");
      musicDock?.classList.toggle("is-playing", playing);
      if (musicStatus) musicStatus.textContent = playing ? "Playing" : "Tap to play";
    };

    const playMusic = async () => {
      try {
        await audio.play();
        syncMusicUI();
        return true;
      } catch (_) {
        syncMusicUI();
        return false;
      }
    };

    const tryAutoplay = async () => {
      const started = await playMusic();
      if (started) return;

      // Most mobile browsers block audible autoplay. Start on the visitor's
      // first intentional interaction while keeping a visible play control.
      const unlock = async () => {
        await playMusic();
        document.removeEventListener("pointerdown", unlock);
        document.removeEventListener("keydown", unlock);
      };
      document.addEventListener("pointerdown", unlock, { once: true });
      document.addEventListener("keydown", unlock, { once: true });
    };

    musicToggle.addEventListener("click", async (event) => {
      event.stopPropagation();
      if (audio.paused) {
        await playMusic();
      } else {
        audio.pause();
        syncMusicUI();
      }
    });

    audio.addEventListener("play", syncMusicUI);
    audio.addEventListener("pause", syncMusicUI);
    audio.addEventListener("ended", syncMusicUI);
    syncMusicUI();
    tryAutoplay();
  }

  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxImage = document.querySelector("[data-lightbox-image]");
  const lightboxCaption = document.querySelector("[data-lightbox-caption]");
  const closeButton = document.querySelector("[data-lightbox-close]");
  const prevButton = document.querySelector("[data-lightbox-prev]");
  const nextButton = document.querySelector("[data-lightbox-next]");
  const galleryImages = [...document.querySelectorAll(".gallery-card img")];

  if (lightbox && lightboxImage && galleryImages.length) {
    let activeIndex = 0;
    let previousFocus = null;

    const render = () => {
      const image = galleryImages[activeIndex];
      const card = image.closest(".gallery-card");
      const caption = card?.querySelector("figcaption")?.textContent?.trim() || image.alt || "";
      lightboxImage.src = image.currentSrc || image.src;
      lightboxImage.alt = image.alt || "Gallery image";
      if (lightboxCaption) lightboxCaption.textContent = caption;
    };

    const open = (index) => {
      activeIndex = index;
      previousFocus = document.activeElement;
      render();
      lightbox.classList.add("is-open");
      lightbox.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      closeButton?.focus();
    };

    const close = () => {
      lightbox.classList.remove("is-open");
      lightbox.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      lightboxImage.src = "";
      if (previousFocus instanceof HTMLElement) previousFocus.focus();
    };

    const step = (direction) => {
      activeIndex = (activeIndex + direction + galleryImages.length) % galleryImages.length;
      render();
    };

    galleryImages.forEach((image, index) => {
      const card = image.closest(".gallery-card");
      if (!card) return;
      card.setAttribute("tabindex", "0");
      card.setAttribute("role", "button");
      card.setAttribute("aria-label", `Open gallery image ${index + 1} of ${galleryImages.length}`);
      card.addEventListener("click", () => open(index));
      card.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          open(index);
        }
      });
    });

    closeButton?.addEventListener("click", close);
    prevButton?.addEventListener("click", () => step(-1));
    nextButton?.addEventListener("click", () => step(1));

    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) close();
    });

    document.addEventListener("keydown", (event) => {
      if (!lightbox.classList.contains("is-open")) return;
      if (event.key === "Escape") close();
      if (event.key === "ArrowLeft") step(-1);
      if (event.key === "ArrowRight") step(1);
    });
  }
})();
