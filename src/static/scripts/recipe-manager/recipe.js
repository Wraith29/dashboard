class RecipePageState {
  /** @type {HTMLInputElement} */
  _servesElement;
  _serves = 0;

  constructor() {
    /** @type {HTMLInputElement | null} */
    const servesElement = document.querySelector("input#serves-value");
    if (servesElement === null) {
      console.error("Unable to find the serves input");
      return;
    }

    this._servesElement = servesElement;
    this._serves = parseInt(servesElement.value);
    this.updateIngredients();
  }

  /**
   * Updates all ingredient quantities, to match the serves multiplier
   * @returns {void}
   */
  updateIngredients() {
    /** @type {NodeListOf<HTMLLIElement> | null} */
    const ingredientsList = document.querySelectorAll("span.ingredient-line");
    if (ingredientsList === null) {
      console.error("No Ingredients Found");
      return;
    }

    for (const ingredient of ingredientsList) {
      /** @type {HTMLElement} */
      const quantityElem = ingredient.querySelector("p.ingredient-quantity");
      const originalQuantity = parseInt(quantityElem.dataset.originalquantity);

      quantityElem.innerText = (originalQuantity * this._serves).toString();
    }
  }

  /**
   * @returns {void}
   */
  decrementServes() {
    if (this._serves > 1) {
      this._serves -= 1;
      this._servesElement.value = this._serves;
    }

    this.updateIngredients();
  }

  /**
   * @returns {void}
   */
  incrementServes() {
    this._serves += 1;
    this._servesElement.value = this._serves;

    this.updateIngredients();
  }
}

/**
 * @param {KeyboardEvent} ev
 */
function handleTagSubmit(ev) {
  const input = ev.target;
  if (input === null) {
    console.error("Tag Input not found");
    return;
  }

  if (input.value.length < 5) {
    input.classList.remove("tag-input-medium", "tag-input-large");
    input.classList.add("tag-input-small");
  } else if (input.value.length >= 5 && input.value.length < 10) {
    input.classList.remove("tag-input-small", "tag-input-large");
    input.classList.add("tag-input-medium");
  } else {
    input.classList.remove("tag-input-small", "tag-input-medium");
    input.classList.add("tag-input-large");
  }

  if (ev.key === "Enter") {
  }
}

/**
 * @returns {void}
 */
function addTag() {
  const tagsList = document.querySelector("ul#recipe-tags-list");
  if (tagsList === null) {
    console.error("Unable to find tags list");
    return;
  }

  const tagInput = document.createElement("input");
  tagInput.type = "text";
  tagInput.classList.add("tag", "tag-input-small");
  tagInput.onkeydown = handleTagSubmit;

  tagsList.append(tagInput);
}

/** @type {RecipePageState} */
let recipePageState;

window.onload = () => {
  recipePageState = new RecipePageState();
};
