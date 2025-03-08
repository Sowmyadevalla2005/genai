function generateActivities() {
    const inputField = document.getElementById('activityInput');
    const outputDiv = document.getElementById('output');
    const scheduleInfoDiv = document.getElementById('schedule-info');
    const scheduleInfoEndDiv = document.getElementById('schedule-info-end');
    const activities = inputField.value.split(',').map(activity => activity.trim());

    if (activities.length === 0 || activities[0] === '') {
      alert('Please enter at least one task.');
      return;
    }

    // Additional line before outputs
    scheduleInfoDiv.innerHTML = "<h4><b>Hey there! <br>This is your schedule for today:</b></h4>";

    let outputHTML = '';

    for (let i = 0; i < activities.length; i++) {
      const outputContainer = document.createElement('div');
      outputContainer.className = 'output-container';
      const fillInTheBlank = `${activities[i]} is your ${i + 1}${getOrdinalSuffix(i + 1)} task!`;
      outputContainer.innerHTML = fillInTheBlank;
      outputDiv.appendChild(outputContainer);
    }

    // Additional line after outputs
    scheduleInfoEndDiv.innerHTML = "<br><h4><b>Good luck finishing them!!<br> Have a great day :)</b></h4>";
  }

  function getOrdinalSuffix(number) {
    const suffixes = ["st", "nd", "rd", "th"];
    const v = number % 100;
    return (v >= 11 && v <= 13) ? 'th' : suffixes[(v - 1) % 10] || 'th';
  }