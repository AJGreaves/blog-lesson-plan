var editButtons = document.getElementsByClassName("btn-edit");
var commentText = document.getElementsByTagName("textarea")[0];
var commentForm = document.getElementById("commentForm");
var submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
var deleteButtons = document.getElementsByClassName("btn-delete");
var deleteConfirm = document.getElementById("deleteConfirm");

/**
 * Add event listeners to comment edit buttons, build the specific link 
 * for each button needed to call the edit view with the correct commentId
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
 * Add event listeners to each comment delete button, set the relevant 
 * attribute value on the modal so that the correct url is accessed to delete
 * the selected comment.
 */
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("comment_id");
        deleteConfirm.href = `delete_comment/${commentId}`;
        deleteModal.show();
    });
}