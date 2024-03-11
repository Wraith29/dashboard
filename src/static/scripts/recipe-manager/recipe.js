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

/** @type {RecipePageState} */
let recipePageState;

window.onload = () => {
  recipePageState = new RecipePageState();
};
