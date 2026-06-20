document.addEventListener("DOMContentLoaded", () => {
    const birthdateInput = document.getElementById("birthdate");
    const targetdateInput = document.getElementById("targetdate");
    const resetBtn = document.getElementById("reset-btn");
    const dateError = document.getElementById("date-error");
    
    const resultsPlaceholder = document.getElementById("results-placeholder");
    const resultsDisplay = document.getElementById("results-display");
    
    const yearsDisplay = document.getElementById("result-years");
    const monthsDisplay = document.getElementById("result-months");
    const daysDisplay = document.getElementById("result-days");
    
    const zodiacEmoji = document.getElementById("zodiac-emoji");
    const zodiacName = document.getElementById("zodiac-name");

    // Initialize target date field to today
    const todayStr = new Date().toISOString().split("T")[0];
    targetdateInput.value = todayStr;

    // Event listeners for date input changes
    birthdateInput.addEventListener("input", handleDateChange);
    targetdateInput.addEventListener("input", handleDateChange);
    
    // Event listener for reset button
    resetBtn.addEventListener("click", resetCalculator);

    let activeController = null;

    async function handleDateChange() {
        const birthdate = birthdateInput.value;
        const targetdate = targetdateInput.value;

        // Abort previous running requests immediately if user types/scrolls calendar rapidly
        if (activeController) {
            activeController.abort();
        }
        activeController = new AbortController();

        // Clear any previous error message
        showError("");

        if (!birthdate) {
            showPlaceholder();
            return;
        }

        // Validate client side first (birthdate must be <= targetdate)
        const selectedDate = new Date(birthdate);
        const targetDate = targetdate ? new Date(targetdate) : new Date();
        // Clear times for direct calendar date comparison
        selectedDate.setHours(0,0,0,0);
        targetDate.setHours(0,0,0,0);

        if (selectedDate > targetDate) {
            showError("Birthdate cannot be after target date");
            showPlaceholder();
            return;
        }

        try {
            const response = await fetch("/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ birthdate, targetdate }),
                signal: activeController.signal
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.error || "An error occurred during calculation");
                showPlaceholder();
                return;
            }

            displayResults(data);

        } catch (err) {
            if (err.name !== "AbortError") {
                console.error("Fetch error:", err);
                showError("Could not connect to the backend calculator service.");
                showPlaceholder();
            }
        }
    }

    function displayResults(data) {
        // Toggle UI states
        resultsPlaceholder.classList.add("hidden");
        resultsDisplay.classList.remove("hidden");

        // Animate count-up of values
        animateValue(yearsDisplay, data.years);
        animateValue(monthsDisplay, data.months);
        animateValue(daysDisplay, data.days);

        // Update Zodiac values
        zodiacEmoji.textContent = data.zodiac_emoji;
        zodiacName.textContent = data.zodiac_name;
    }

    function animateValue(element, targetValue) {
        // Cancel any previous interval running on this element
        if (element.dataset.intervalId) {
            clearInterval(parseInt(element.dataset.intervalId, 10));
        }

        if (targetValue === 0) {
            element.textContent = "0";
            return;
        }

        let startValue = 0;
        const duration = 500; // Animation duration in milliseconds
        const fps = 30;
        const steps = Math.max(10, Math.ceil(duration / (1000 / fps)));
        const increment = targetValue / steps;
        
        let stepCount = 0;

        const intervalId = setInterval(() => {
            stepCount++;
            startValue += increment;
            
            if (stepCount >= steps || startValue >= targetValue) {
                element.textContent = targetValue;
                clearInterval(intervalId);
                element.removeAttribute("data-interval-id");
            } else {
                element.textContent = Math.floor(startValue);
            }
        }, 1000 / fps);

        element.dataset.intervalId = intervalId.toString();
    }

    function showError(message) {
        dateError.textContent = message;
        if (message) {
            dateError.style.opacity = "1";
            birthdateInput.setAttribute("aria-invalid", "true");
            birthdateInput.setAttribute("aria-describedby", "date-error");
        } else {
            dateError.style.opacity = "0";
            birthdateInput.removeAttribute("aria-invalid");
            birthdateInput.removeAttribute("aria-describedby");
        }
    }

    function showPlaceholder() {
        resultsDisplay.classList.add("hidden");
        resultsPlaceholder.classList.remove("hidden");
    }

    function resetCalculator() {
        birthdateInput.value = "";
        targetdateInput.value = todayStr;
        showError("");
        showPlaceholder();
    }
});
