/* DOM rendering functions */
import { state } from "./state.js"

export function renderContactList(contacts, onClick) {
    const list = document.getElementById("contact-list");
    list.innerHTML = "";

    contacts.forEach(c => {
        const li = document.createElement("li");
        li.textContent = `${c.first_name} ${c.last_name}`;
        li.onclick = () => onClick(c.id);
        list.appendChild(li);
    });
}

export function renderContactDetails(contact, handlers) {
  const container = document.getElementById("contact-details");

  if (state.isEditing) {
    renderEditMode(container, contact, handlers);
  }
  else {
    renderViewMode(container, contact, handlers);
  }
}

function renderViewMode(container, contact, { onEdit }) {
  // html for contact details view mode
  container.innerHTML = `
      <h2>${contact.first_name} ${contact.middle_name_init || ""} ${contact.last_name}</h2>
      <p>Birthday: ${contact.birthday || ""}</p>

      <h3>Email Addresses</h3>
      <ul>
        ${contact.e_addresses.map(e => `<li>${e}</li>`).join("")}
      </ul>

      <button type="button" id="edit-btn" class="edit-btn">Edit</button>
    `;

    // attach event listener to edit button
    document.getElementById("edit-btn").addEventListener("click", onEdit);
}

function renderEditMode(container, contact, { onSave, onDelete, onCancel }) {
  // html for contact details edit mode
  container.innerHTML = `
      <form id="edit-form">
        <input 
          type="text"
          name="first_name"
          placeholder=${contact.first_name}
          class="edit-input"
        ><input
          type="text"
          name="middle_name_init"
          placeholder=${contact.middle_name_init || "Middle Name/Init"}
          class="edit-input"
        ><input
          type="text"
          name="last_name"
          placeholder=${contact.last_name}
          class="edit-input"
        >

        <p>Birthday: <input
          type="date"
          name="birthday"
        ></p>
      
        <h3>Email Addresses</h3>
        <ul>
          ${(contact.e_addresses ?? []).map(e => `<li>${e}</li>`).join("")}
        </ul>

        <button 
          type="button" id="delete-btn" class="edit-btn"
        >Delete</button> <button 
          type="button" id="cancel-btn" class="edit-btn"
        >Cancel</button> <button 
          type="submit" class="edit-btn"
        >Save</button>

      </form>
    `;

  // attach event listener's to buttons
  document.getElementById("edit-form").addEventListener("submit", onSave);
  document.getElementById("delete-btn").addEventListener("click", onDelete);
  document.getElementById("cancel-btn").addEventListener("click", onCancel);
}