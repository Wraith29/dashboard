//@ts-check

class RecipeFormException extends Error {}

/**
 *
 * @param {string} elementId
 * @param {Document} doc
 * @returns {string}
 */
function getElementValue(elementId, doc) {
  /** @type {HTMLInputElement | null} */
  const element = doc.querySelector(elementId);
  if (!element) {
    console.error(`Unable to find ${elementId}`);
    throw new RecipeFormException(elementId);
  }

  const value = element.value;
  if (!value) {
    console.error(`Unable to get value from ${element}`);
    throw new RecipeFormException(elementId);
  }

  return value;
}

/**
 * @typedef Ingredient
 * @prop {string} name
 * @prop {number} quantity
 * @prop {string} measurement
 */

/**
 * @returns {Promise<void>}
 */
async function submitRecipe() {
  const name = getElementValue("input#recipe-name-input", document);
  const description = getElementValue("textarea#recipe-desc-input", document);
  const serves = parseInt(
    getElementValue("input#recipe-serves-input", document)
  );

  /** @type {NodeListOf<HTMLDivElement>} */
  const ingredientElements = document.querySelectorAll("div.ingredient-row");
  /** @type {Array<Ingredient>} */
  const ingredientValues = [];

  for (const [index, ingElem] of ingredientElements.entries()) {
    const ingName = getElementValue(
      `input#recipe-ing-name-input-${index}`,
      ingElem.ownerDocument
    );

    const ingQuantity = parseInt(
      getElementValue(
        `input#recipe-ing-quantity-input-${index}`,
        ingElem.ownerDocument
      )
    );

    const ingMeasurement = getElementValue(
      `input#recipe-ing-measurement-input-${index}`,
      ingElem.ownerDocument
    );

    ingredientValues.push({
      name: ingName,
      quantity: ingQuantity,
      measurement: ingMeasurement,
    });
  }

  /** @type {NodeListOf<HTMLDivElement>} */
  const instructionElements = document.querySelectorAll("div.instruction-row");
  /** @type {Array<string>} */
  const instructionValues = [];

  for (const [index, instElem] of instructionElements.entries()) {
    const instruction = getElementValue(
      `input#recipe-inst-input-${index}`,
      instElem.ownerDocument
    );

    instructionValues.push(instruction);
  }

  await fetch("/api/recipe/create", {
    method: "POST",
    body: JSON.stringify({
      name: name,
      description: description,
      serves: serves,
      ingredients: ingredientValues,
      instructions: instructionValues,
      tags: [],
    }),
  });

  window.location.replace("/recipe-manager");
}

/**
 * @typedef InputList
 * @prop {HTMLDivElement} parentElement the element to hold all the elements within
 * @prop {number} count the number of elements currently available
 * @prop {number} id the current max id
 */

class CreatePageState {
  /** @type {InputList} */
  _ingredients;

  /** @type {InputList} */
  _instructions;

  constructor() {
    /** @type {HTMLDivElement | null} */
    const ingredientsElement = document.querySelector("div#ingredients-block");
    if (ingredientsElement === null) {
      console.error("Unable to find the ingredients block");
      return;
    }
    this._ingredients = {
      parentElement: ingredientsElement,
      count: 0,
      id: 0,
    };

    /** @type {HTMLDivElement | null} */
    const instructionsElement = document.querySelector(
      "div#instructions-block"
    );
    if (instructionsElement === null) {
      console.error("Unable to find the instructions block");
      return;
    }
    this._instructions = {
      parentElement: instructionsElement,
      count: 0,
      id: 0,
    };

    this.addIngredient();
    this.addInstruction();
  }

  /**
   * Update all ingredient rows, to ensure + / - buttons are there where needed
   * @returns {void}
   */
  updateIngredients() {
    /** @type {NodeListOf<HTMLElement>} */
    const ingredientRows = document.querySelectorAll("div.ingredient-row");

    // If there are multiple ingredients, we want them all to be removable
    if (this._ingredients.count > 1) {
      for (const row of ingredientRows) {
        if (!row.querySelector("i.ing-remove-btn")) {
          const rawId = row.dataset.id;
          if (!rawId) {
            console.error(`Row ${row} missing data-id`);
            continue;
          }
          const id = parseInt(rawId);

          const removeBtn = this.createIngredientRemoveButton(id);

          row.appendChild(removeBtn);
        }
      }

      return;
    }

    // There is only 1 row (easier to just iterate over the 1)
    // And we don't want the user to be able to remove it
    for (const row of ingredientRows) {
      const removeBtn = row.querySelector("i.ing-remove-btn");

      if (removeBtn) {
        row.removeChild(removeBtn);
      }
    }
  }

  /**
   * Update all ingredient rows, to ensure + / - buttons are there where needed
   * @returns {void}
   */
  updateInstructions() {
    /** @type {NodeListOf<HTMLElement>} */
    const instructionRows = document.querySelectorAll("div.instruction-row");

    // If there are multiple instructions, we want them all to be removable
    if (this._instructions.count > 1) {
      for (const row of instructionRows) {
        if (!row.querySelector("i.inst-remove-btn")) {
          const rawId = row.dataset.id;
          if (!rawId) {
            console.error(`Row ${row} missing data-id`);
            continue;
          }
          const id = parseInt(rawId);

          const removeBtn = this.createInstructionRemoveButton(id);

          row.appendChild(removeBtn);
        }
      }

      return;
    }

    // There is only 1 row (easier to just iterate over the 1)
    // And we don't want the user to be able to remove it
    for (const row of instructionRows) {
      const removeBtn = row.querySelector("i.inst-remove-btn");

      if (removeBtn) {
        row.removeChild(removeBtn);
      }
    }
  }

  /**
   * Generates a HTML Element for a remove button for the given ingredient row id
   * @param {number} ingredientId
   * @returns {HTMLElement}
   */
  createIngredientRemoveButton(ingredientId) {
    const elem = document.createElement("i");

    elem.classList.add(
      "ing-btn",
      "ing-remove-btn",
      "fa-solid",
      "fa-circle-minus"
    );
    elem.onclick = () => createPageState.removeIngredient(ingredientId);
    return elem;
  }

  /**
   * Generates a HTML Element for a remove button for the given ingredient row id
   * @param {number} instructionId
   * @returns {HTMLElement}
   */
  createInstructionRemoveButton(instructionId) {
    const elem = document.createElement("i");

    elem.classList.add(
      "inst-btn",
      "inst-remove-btn",
      "fa-solid",
      "fa-circle-minus"
    );
    elem.onclick = () => createPageState.removeInstruction(instructionId);
    return elem;
  }

  /**
   * Add a new ingredient row
   * @returns {void}
   */
  addIngredient() {
    const currentId = this._ingredients.id;
    this._ingredients.count += 1;
    this._ingredients.id += 1;

    const formRow = document.createElement("div");
    formRow.classList.add("form-row", "ingredient-row");
    formRow.id = `ingredient-${currentId}`;
    formRow.dataset.id = currentId.toString();

    const ingName = document.createElement("input");
    ingName.classList.add("recipe-ing-name", "ing-input");
    ingName.id = `recipe-ing-name-input-${currentId}`;
    ingName.type = "text";
    ingName.placeholder = "Ingredient";

    formRow.appendChild(ingName);

    const ingQuantity = document.createElement("input");
    ingQuantity.classList.add("recipe-ing-quantity", "ing-input");
    ingQuantity.id = `recipe-ing-quantity-input-${currentId}`;
    ingQuantity.type = "text";
    ingQuantity.inputMode = "numeric";
    ingQuantity.value = "1";

    formRow.appendChild(ingQuantity);

    const ingMeasurement = document.createElement("input");
    ingMeasurement.classList.add("recipe-ing-measurement", "ing-input");
    ingMeasurement.id = `recipe-ing-measurement-input-${currentId}`;
    ingMeasurement.type = "text";
    ingMeasurement.placeholder = "Measurement";

    formRow.appendChild(ingMeasurement);

    const newIngButton = document.createElement("i");
    newIngButton.classList.add(
      "ing-btn",
      "ing-add-btn",
      "fa-solid",
      "fa-circle-plus"
    );
    newIngButton.onclick = () => createPageState.addIngredient();

    formRow.appendChild(newIngButton);

    if (this._ingredients.count > 1) {
      const removeIngButton = this.createIngredientRemoveButton(currentId);
      formRow.appendChild(removeIngButton);
    }

    this._ingredients.parentElement.append(formRow);

    this.updateIngredients();
  }

  /**
   * Add a new instruction row
   * @returns {void}
   */
  addInstruction() {
    const currentId = this._instructions.id;
    this._instructions.count += 1;
    this._instructions.id += 1;

    const formRow = document.createElement("div");
    formRow.classList.add("form-row", "instruction-row");
    formRow.id = `instruction-${currentId}`;
    formRow.dataset.id = currentId.toString();

    const instName = document.createElement("input");
    instName.classList.add("recipe-inst");
    instName.id = `recipe-inst-input-${currentId}`;
    instName.type = "text";
    instName.placeholder = "Instruction";

    formRow.appendChild(instName);

    const newIngButton = document.createElement("i");
    newIngButton.classList.add(
      "ing-btn",
      "ing-add-btn",
      "fa-solid",
      "fa-circle-plus"
    );
    newIngButton.onclick = () => createPageState.addInstruction();

    formRow.appendChild(newIngButton);

    if (this._instructions.count > 1) {
      const removeIngButton = this.createInstructionRemoveButton(currentId);
      formRow.appendChild(removeIngButton);
    }

    this._instructions.parentElement.append(formRow);

    this.updateInstructions();
  }

  /**
   * Remove an ingredient from the recipe
   * @param {number} ingredientId
   * @returns {void}
   */
  removeIngredient(ingredientId) {
    const ingredientRow = document.querySelector(
      `div#ingredient-${ingredientId}`
    );

    ingredientRow?.remove();
    this._ingredients.count -= 1;

    this.updateIngredients();
  }

  /**
   * Remove an instruction from the recipe
   * @param {number} instructionId
   * @returns {void}
   */
  removeInstruction(instructionId) {
    const instructionRow = document.querySelector(
      `div#instruction-${instructionId}`
    );

    instructionRow?.remove();
    this._instructions.count -= 1;

    this.updateInstructions();
  }
}

/** @type {CreatePageState} */
let createPageState;

window.onload = function () {
  createPageState = new CreatePageState();
};
