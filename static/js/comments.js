var editButtons = document.getElementsByClassName("btn-edit");
var commentText = document.getElementsByTagName("textarea")[0];
var commentForm = document.getElementById("commentForm");
var submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
var deleteButtons = document.getElementsByClassName("btn-delete");
var deleteConfirm = document.getElementById("deleteConfirm");

/**
 * When any button from the editButtons collection is clicked, the code:
 * Retrieves the associated comment ID.
 * Fetches the content of the corresponding comment.
 * Populates a form with this content for editing.
 * Changes the submit button's text to indicate an update.
 * Updates the form's action to point to an endpoint for editing the comment with the respective ID.
 */
for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("comment_id");
        let commentContent = document.getElementById(`comment${commentId}`).innerText;
        commentText.value = commentContent;
        submitButton.innerText = "Update";
        commentForm.setAttribute("action", `edit_comment/${commentId}`);
    });
}


/**
 * when any button from the deleteButtons collection is clicked, the code:
 * Retrieves the comment ID associated with the clicked button.
 * Updates a link's href to point to a URL for deleting the comment with the given ID.
 * Displays a confirmation modal to the user.
 */
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("comment_id");
        deleteConfirm.href = `delete_comment/${commentId}`;
        deleteModal.show();
    });
}