document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const submitBtn = document.getElementById("submitBtn");
  const successMessage = document.getElementById("successMessage");

  if (!form || !submitBtn) return;

  form.addEventListener("submit", function (event) {
    submitBtn.innerText = "Submitting...";
    submitBtn.disabled = true;
    submitBtn.classList.add("opacity-70", "cursor-not-allowed");

    // Optional visual feedback (frontend only)
    setTimeout(() => {
      if (successMessage) {
        successMessage.classList.remove("hidden");
      }
    }, 500);
  });
});

