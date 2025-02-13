document.getElementById("addTaskButton").addEventListener("click", addItem);

let taskCount = 0; // Tracks the number of tasks

function addItem() {
    let input = document.getElementById("addTask");
    let text = input.value.trim();

    if (text === "") return; 

    let list = document.getElementById("list");

    let li = document.createElement("li");
    li.className = "list-item";
    li.style.top = `${150 + taskCount * 70}px`; // Position each task dynamically
    li.innerHTML = `${text} <button class="delete-btn">Delete</button>`;

    // Add delete button functionality
    li.querySelector(".delete-btn").addEventListener("click", function () {
        li.remove();
        reorderTasks(); 
    });

    list.appendChild(li);
    taskCount++; 
    input.value = ""; 
}

// Function to reorder tasks after deletion
function reorderTasks() {
    let tasks = document.querySelectorAll(".list-item");
    taskCount = 0; 
    tasks.forEach(task => {
        task.style.top = `${150 + taskCount * 70}px`; // Recalculate positions
        taskCount++;
    });
}
