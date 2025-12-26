const ACCESS_CODE = "1234";

const overlay = document.getElementById("overlay");
const content = document.getElementById("content");
const input = document.getElementById("codeInput");
const btn = document.getElementById("unlockBtn");
const err = document.getElementById("lockError");

function unlock(){
  const val = (input.value || "").trim();
  if (val === ACCESS_CODE){
    // Overlay disparaît, l'intro est déjà en dessous
    overlay.classList.add("is-hidden");

    // Init stack animations
    initStack();

    // On remet le scroll en haut (dans le container)
    content.scrollTo({ top: 0, behavior: "instant" });
  } else {
    err.textContent = "Mauvais code.";
    input.focus();
    input.select?.();
  }
}
btn.addEventListener("click", unlock);
input.addEventListener("keydown", (e) => { if (e.key === "Enter") unlock(); });

function initStack(){
  const frames = Array.from(document.querySelectorAll(".frame"));

  // Captions + direction alternée
  frames.forEach((frame, idx) => {
    const capText = frame.getAttribute("data-caption") || "";

    const cap = document.createElement("div");
    cap.className = "caption";
    cap.textContent = capText;
    if (!capText.trim()) cap.style.display = "none";
    frame.appendChild(cap);

    // Alternance gauche/droite
    // idx 0 => droite, idx 1 => gauche, etc.
    const fromRight = idx % 2 === 0;
    frame.style.setProperty("--fromX", fromRight ? "40px" : "-40px");
  });

  // Reveal quand la slide devient dominante dans le viewport du container
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting){
        entry.target.classList.add("reveal");
      }
    });
  }, {
    root: content,
    threshold: 0.7
  });

  frames.forEach(f => io.observe(f));

  // Preload (évite flash/noir)
  const urls = frames.map(f => {
    const raw = getComputedStyle(f).getPropertyValue("--img").trim();
    return raw.replace(/^url\(["']?/, "").replace(/["']?\)$/, "");
  });
  urls.forEach(u => { const img = new Image(); img.src = u; });
}
