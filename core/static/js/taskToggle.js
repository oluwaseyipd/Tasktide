// Enhanced JavaScript with smooth disappear animation
document.addEventListener("change", function (e) {
  if (e.target.matches(".task-toggle")) {
    const taskId = e.target.dataset.taskId;
    toggleTask(taskId, e.target.checked);
  }
});

function toggleTask(taskId, isChecked) {
  fetch(`/tasks/${taskId}/toggle/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ completed: isChecked }),
  })
    .then((r) => r.json())
    .then((data) => {
      if (!data.success) return alert("Something went wrong");

      const card = document.querySelector(`#task-${taskId}`);
      const title = card?.querySelector("h3");

      if (data.completed) {
        title?.classList.add("line-through");

        // Play sound first
        const sound = document.getElementById("pop-sound");
        sound?.play();

        // Add fade-out animation
        if (card) {
          // Add the fade-out class
          card.classList.add('task-fade-out');
          
          // Wait for animation to complete, then hide the element
          setTimeout(() => {
            card.style.display = 'none';
            // Optional: Update the task count display
            updateTaskCount();
          }, 500); // Match this with your CSS transition duration
        }
      } else {
        title?.classList.remove("line-through");
        
        // If unchecking, show the card again
        if (card) {
          card.style.display = 'block';
          card.classList.remove('task-fade-out');
          // Optional: Update the task count display
          updateTaskCount();
        }
      }
    })
    .catch(console.error);
}

// Optional: Function to update task count
function updateTaskCount() {
  const visibleTasks = document.querySelectorAll('.task-card:not([style*="display: none"])');
  const countElement = document.querySelector('.text-sm.text-gray-600');
  if (countElement) {
    countElement.textContent = `Showing ${visibleTasks.length} tasks`;
  }
}

// CSRF helper
function getCookie(name) {
  let value = null;
  if (document.cookie && document.cookie !== "") {
    document.cookie.split(";").forEach((cookie) => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        value = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return value;
}