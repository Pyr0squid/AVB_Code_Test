/* DOM rendering functions */
import { state } from "./state.js";

export function renderContactList(contacts, onClick) {
  const list = document.getElementById("contact-list");
  list.innerHTML = "";

  if (contacts) {
    contacts.forEach((c) => {
      const li = document.createElement("li");
      li.textContent = `${c.first_name} ${c.last_name}`;
      li.onclick = () => onClick(c.id);
      list.appendChild(li);
    });
  }
}

export function renderContactDetails(contact, handlers) {
  const container = document.getElementById("contact-details");

  if (state.isEditing) {
    renderEditMode(container, contact, handlers);
  } else {
    renderViewMode(container, contact, handlers);
  }
}

function renderViewMode(container, contact, { onEdit }) {
  // Format birthday from yyyy-mm-dd to dd/mm/yyyy
  let displayBirthday = "";
  if (contact.birthday) {
    const [year, month, day] = contact.birthday.split("-");
    displayBirthday = `${month}/${day}/${year}`;
  }

  // html for contact details view mode
  container.innerHTML = `
      <h2>${contact.first_name} ${contact.middle_name_init || ""} ${contact.last_name}</h2>
      <p>Birthday: ${displayBirthday}</p>

      <h3>Email Addresses</h3>
      <ul>
        ${contact.e_addresses.map((e) => `<li>${e}</li>`).join("")}
      </ul>

      <button type="button" id="edit-btn" class="edit-btn">Edit</button>
    `;

  // attach event listener to edit button
  document.getElementById("edit-btn").addEventListener("click", onEdit);
}

function renderEditMode(
  container,
  contact,
  { onSave, onDelete, onCancel, onAddEmail, onDeleteEmail },
) {
  container.innerHTML = `
      <form id="edit-form">
        <input type="text" name="first_name" placeholder="${contact.first_name}" class="edit-input">
        <input type="text" name="middle_name_init" placeholder="${contact.middle_name_init || "Middle"}" class="edit-input">
        <input type="text" name="last_name" placeholder="${contact.last_name}" class="edit-input">

        <p>Birthday: <input type="date" name="birthday" value="${contact.birthday || ""}"></p>
      
        <h3>Email Addresses</h3>
        <div id="edit-email-list">
          ${(contact.e_addresses ?? [])
            .map(
              (e) => `
            <div class="email-item-container">
              <span>${e}</span>
              <button type="button" class="delete-addr-btn" data-email="${e}">X</button>
            </div>
          `,
            )
            .join("")}
        </div>
        
        <div id="new-emails-container"></div>
        <button type="button" id="add-email-edit-btn">+ Add Email</button>

        <hr>
        <button type="button" id="delete-btn" class="edit-btn">Delete Contact</button> 
        <button type="button" id="cancel-btn" class="edit-btn">Cancel</button> 
        <button type="submit" class="edit-btn">Save</button>
      </form>
    `;

  // Attach listeners
  document.getElementById("edit-form").addEventListener("submit", onSave);
  document.getElementById("delete-btn").addEventListener("click", onDelete);
  document.getElementById("cancel-btn").addEventListener("click", onCancel);

  // New listeners for email management
  document
    .getElementById("add-email-edit-btn")
    .addEventListener("click", onAddEmail);

  // Delegate delete clicks
  document.querySelectorAll(".delete-addr-btn").forEach((btn) => {
    btn.addEventListener("click", () => onDeleteEmail(btn.dataset.email));
  });
}
