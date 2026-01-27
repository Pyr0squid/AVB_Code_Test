const contactList = document.getElementById("contact-list");
const contactDetails = document.getElementById("contact-details");

/* Load contact names on page load */
fetch("/api/names")
    .then(res => res.json())
    .then(contacts => {
        contacts.forEach(contact => {
            const li = document.createElement("li");
            li.textContent = `${contact.first_name} ${contact.last_name}`;
            li.dataset.id = contact.id;

            li.addEventListener("click", () => selectContact(li));

            contactList.appendChild(li);
        });
    })
    .catch(err => console.error(err));


function selectContact(element) {
    // highlight selected
    document.querySelectorAll("#contact-list li")
        .forEach(li => li.classList.remove("active"));

    element.classList.add("active");

    const id = element.dataset.id;

    fetch(`/api/retrieve/${id}`)
        .then(res => res.json())
        .then(contact => renderContact(contact))
        .catch(err => console.error(err));
}


function renderContact(contact) {
    contactDetails.innerHTML = `
        <div class="field"><strong>First Name:</strong> ${contact.first_name}</div>
        <div class="field"><strong>Middle Initial:</strong> ${contact.middle_name_init ?? ""}</div>
        <div class="field"><strong>Last Name:</strong> ${contact.last_name}</div>
        <div class="field"><strong>Birthday:</strong> ${contact.birthday ?? ""}</div>

        <h3>Email Addresses</h3>
        <ul>
            ${contact.e_addresses.map(addr => `<li>${addr}</li>`).join("")}
        </ul>
    `;
}

const modalOverlay = document.getElementById("modal-overlay");
const createContactBtn = document.getElementById("create-contact-btn");
const cancelBtn = document.getElementById("cancel-btn");

createContactBtn.addEventListener("click", () => {
    modalOverlay.classList.remove("hidden");
});

cancelBtn.addEventListener("click", () => {
    closeModal();
});

function closeModal() {
    modalOverlay.classList.add("hidden");
    document.getElementById("create-contact-form").reset();
    document.getElementById("email-list").innerHTML = "";
}

const emailList = document.getElementById("email-list");
const addEmailBtn = document.getElementById("add-email-btn");

addEmailBtn.addEventListener("click", () => {
    addEmailField();
});

function addEmailField(value = "") {
    const row = document.createElement("div");
    row.className = "email-row";

    const input = document.createElement("input");
    input.type = "email";
    input.placeholder = "email@example.com";
    input.value = value;

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.textContent = "✖";
    removeBtn.addEventListener("click", () => row.remove());

    row.appendChild(input);
    row.appendChild(removeBtn);
    emailList.appendChild(row);
}

const createContactForm = document.getElementById("create-contact-form");

createContactForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(createContactForm);

    const emails = [...emailList.querySelectorAll("input")]
        .map(input => input.value)
        .filter(val => val !== "");

    const payload = {
        first_name: formData.get("first_name"),
        middle_name_init: formData.get("middle_name_init"),
        last_name: formData.get("last_name"),
        birthday: formData.get("birthday"),
        e_addresses: emails
    };

    fetch("/api/add/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to create contact");
        return res.json();
    })
    .then(() => {
        closeModal();
        location.reload(); // simple refresh for now
    })
    .catch(err => alert(err.message));
});
