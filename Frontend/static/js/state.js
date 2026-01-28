/* selected contact, edit mode, and cache */

export const state = {
    selectedContact: null,
    isEditing: false
};

export function setSelectedContact(contact) {
    state.selectedContact = contact;
}

export function setEditing(value) {
    state.isEditing = value;
}
