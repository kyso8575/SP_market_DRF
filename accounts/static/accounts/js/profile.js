async function handleFollowToggle(button) {
  const form = button.closest("form");
  const actionUrl = form.getAttribute("data-action-url");
  const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;

  try {
    const response = await fetch(actionUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      if (button.classList.contains("btn-follow")) {
        button.classList.replace("btn-follow", "btn-unfollow");
        button.textContent = "Unfollow";
        form.setAttribute(
          "data-action-url",
          actionUrl.replace("follow", "unfollow")
        );
      } else {
        button.classList.replace("btn-unfollow", "btn-follow");
        button.textContent = "Follow";
        form.setAttribute(
          "data-action-url",
          actionUrl.replace("unfollow", "follow")
        );
      }
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
