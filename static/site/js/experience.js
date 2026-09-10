(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const intro = document.querySelector("[data-cinematic-intro]");
  const introSkip = document.querySelector("[data-intro-skip]");

  if (intro) {
    const storageKey = intro.dataset.introKey || "celebrationIntroSeen";
    const dismissIntro = () => {
      intro.classList.add("is-hidden");
      document.body.classList.remove("intro-active");
      intro.setAttribute("aria-hidden", "true");
      try {
        sessionStorage.setItem(storageKey, "1");
      } catch (_) {}
      window.setTimeout(() => intro.remove(), reduceMotion ? 0 : 850);
    };

    let seen = false;
    try {
      seen = sessionStorage.getItem(storageKey) === "1";
    } catch (_) {}

    if (seen || reduceMotion) {
      dismissIntro();
    } else {
      document.body.classList.add("intro-active");
      intro.setAttribute("aria-hidden", "false");
      const timer = window.setTimeout(dismissIntro, 2800);
      introSkip?.addEventListener("click", () => {
        window.clearTimeout(timer);
        dismissIntro();
      }, { once: true });
    }
  }

  const audio = document.querySelector("[data-background-music]");
  const musicToggle = document.querySelector("[data-music-toggle]");
  const musicDock = document.querySelector("[data-music-dock]");
  const musicStatus = document.querySelector("[data-music-status]");
  const autoplayGate = document.querySelector("[data-music-autoplay-gate]");
  const musicStart = document.querySelector("[data-music-start]");

  if (audio && musicToggle) {
    const configuredVolume = Number.parseInt(audio.dataset.musicVolume || "55", 10);
    const safeVolume = Number.isFinite(configuredVolume) ? configuredVolume : 55;
    const wantsAutoplay = audio.dataset.musicAutoplay === "true";
    const reduceMusicMotion = reduceMotion ? 0 : 460;
    let gateHideTimer = null;
    let userPaused = false;

    audio.volume = Math.min(1, Math.max(0, safeVolume / 100));

    const showAutoplayGate = () => {
      if (!autoplayGate || !musicStart || !wantsAutoplay || userPaused || audio.error) return;
      if (gateHideTimer) window.clearTimeout(gateHideTimer);
      autoplayGate.hidden = false;
      autoplayGate.setAttribute("aria-hidden", "false");
      document.body.classList.add("music-gate-active");
      window.requestAnimationFrame(() => {
        if (autoplayGate.hidden || !audio.paused) return;
        autoplayGate.classList.add("is-visible");
        musicStart.focus({ preventScroll: true });
      });
      if (musicStatus) musicStatus.textContent = "Tap to start";
    };

    const hideAutoplayGate = () => {
      if (!autoplayGate) return;
      autoplayGate.classList.remove("is-visible");
      autoplayGate.setAttribute("aria-hidden", "true");
      document.body.classList.remove("music-gate-active");
      if (gateHideTimer) window.clearTimeout(gateHideTimer);
      gateHideTimer = window.setTimeout(() => {
        autoplayGate.hidden = true;
      }, reduceMusicMotion);
    };

    const syncMusicUI = () => {
      const playing = !audio.paused && !audio.ended;
      musicToggle.setAttribute("aria-pressed", String(playing));
      musicToggle.setAttribute("aria-label", playing ? "Pause background music" : "Play background music");
      musicDock?.classList.toggle("is-playing", playing);
      if (musicStatus) musicStatus.textContent = playing ? "Playing" : "Tap to play";
      if (playing) hideAutoplayGate();
    };

    const playMusic = async ({ showFallback = false } = {}) => {
      if (audio.error) {
        hideAutoplayGate();
        if (musicStatus) musicStatus.textContent = "Audio unavailable";
        return false;
      }

      audio.muted = false;
      try {
        await audio.play();
        syncMusicUI();
        return true;
      } catch (error) {
        syncMusicUI();
        if (audio.error) {
          hideAutoplayGate();
          if (musicStatus) musicStatus.textContent = "Audio unavailable";
        } else if (showFallback && error?.name !== "NotSupportedError") {
          showAutoplayGate();
        }
        return false;
      }
    };

    const tryAutoplay = async () => {
      if (!wantsAutoplay || userPaused || !audio.paused) return;
      await playMusic({ showFallback: true });
    };

    musicToggle.addEventListener("click", async (event) => {
      event.stopPropagation();
      if (audio.paused) {
        userPaused = false;
        await playMusic();
      } else {
        userPaused = true;
        audio.pause();
      }
      syncMusicUI();
    });

    const startFromVisitorGesture = async () => {
      userPaused = false;
      await playMusic({ showFallback: true });
    };

    musicStart?.addEventListener("click", startFromVisitorGesture);
    autoplayGate?.addEventListener("click", (event) => {
      if (event.target === autoplayGate) startFromVisitorGesture();
    });

    audio.addEventListener("play", syncMusicUI);
    audio.addEventListener("pause", syncMusicUI);
    audio.addEventListener("ended", () => {
      userPaused = true;
      syncMusicUI();
    });
    audio.addEventListener("error", () => {
      hideAutoplayGate();
      syncMusicUI();
      if (musicStatus) musicStatus.textContent = "Audio unavailable";
    });
    window.addEventListener("pageshow", tryAutoplay);
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible") tryAutoplay();
    });

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
