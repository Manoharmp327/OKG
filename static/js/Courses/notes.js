let editorInstance;

// Open the note editor for a new note
function openNoteEditor(subtitleId, subtitleName) {
  document.getElementById("note-editor-heading").textContent =
    subtitleName + " Notes";
  document.getElementById("note-editor-container").style.display = "block";

  initializeEditor("");
  setHiddenInput("subtitle_id", subtitleId);
}

// Open the editor to edit an existing note
function editNote(noteId, noteTitle, noteContent) {
  document.getElementById("note-editor-heading").textContent =
    "Edit Note: " + noteTitle;
  document.getElementById("note-editor-container").style.display = "block";

  initializeEditor(noteContent);
  setHiddenInput("note_id", noteId);
}

// Initialize CKEditor with optional content
function initializeEditor(content = "") {
  if (editorInstance) {
    editorInstance.destroy().catch((error) => console.error(error));
  }

  ClassicEditor.create(document.getElementById("editor"))
    .then((editor) => {
      editorInstance = editor;
      editor.setData(content);
    })
    .catch((error) => {
      console.error(error);
    });
}

// Add or update hidden input for subtitle_id or note_id
function setHiddenInput(name, value) {
  const form = document.getElementById("note-form");
  let input = form.querySelector(`input[name="${name}"]`);

  if (!input) {
    input = document.createElement("input");
    input.type = "hidden";
    input.name = name;
    form.appendChild(input);
  }

  input.value = value;
}

// Delete a note
function deleteNote(noteId) {
  if (!confirm("Are you sure you want to delete this note?")) {
    return;
  }

  fetch("{% url 'delete_note' %}", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({ note_id: noteId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Note deleted successfully!");
        window.location.reload();
      } else {
        alert(`Error deleting note: ${data.error}`);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while deleting the note.");
    });
}

// Handle form submission for creating or editing notes
const form = document.getElementById("note-form");
form.onsubmit = function (event) {
  event.preventDefault();

  const content = editorInstance.getData();
  const subtitleId = form.querySelector('input[name="subtitle_id"]')
    ? form.querySelector('input[name="subtitle_id"]').value
    : null;
  const noteId = form.querySelector('input[name="note_id"]')
    ? form.querySelector('input[name="note_id"]').value
    : null;

  if (!content.trim()) {
    alert("Content cannot be empty.");
    return;
  }

  const url = noteId ? "{% url 'update_note' %}" : "{% url 'create_note' %}";

  const data = {
    content: content,
  };

  if (subtitleId) {
    data.subtitle_id = subtitleId;
  }

  if (noteId) {
    data.note_id = noteId;
  }

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Note saved successfully!");
        document.getElementById("note-editor-container").style.display = "none";
        form.reset();
        window.location.reload();
      } else {
        alert(`Error saving note: ${data.error}`);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while saving the note.");
    });
};
