// @ts-check

/**
 * @returns {Promise<void>}
 */
async function submit() {
  /** @type {HTMLInputElement | null} */
  const inputElement = document.querySelector("input#artist-name-input");
  if (inputElement === null) {
    console.error("Input element not found");
    return;
  }

  const artistName = inputElement.value;

  await fetch("/api/setlist-generator/create-setlist", {
    method: "POST",
    body: JSON.stringify({
      name: artistName,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (res.headers.get("Content-Type") === "application/json") {
        return res.json();
      }
      return { "": "" };
    })
    .then((data) => {
      if ("redirect_uri" in data) {
        window.location.href = data.redirect_uri;
      }
    });
}
