  document.querySelector("#add-question").addEventListener("click", () => {
        fetch('add_question', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            let ele = document.createElement('div')
            ele.classList.add('margin-top-bottom');
            ele.classList.add('box');
            ele.classList.add('question-box');
            ele.classList.add('question');
            ele.setAttribute("data-id", result["question"].id)
            ele.innerHTML = `
            <input type="text" data-id="${result["question"].id}" class="question-title edit-on-click input-question" value="${result["question"].question}">
            <select class="question-type-select input-question-type" data-id="${result["question"].id}" data-origin_type = "${result["question"].question_type}">
                <option value="short">Short answer</option>
                <option value="paragraph">Paragraph</option>
                <option value="multiple choice" selected>Multiple choice</option>
                <option value="checkbox">Checkbox</option>
            </select>
            <div class="choices" data-id="${result["question"].id}">
                <div class="choice">
                    <input type="radio" id="${result["choices"].id}" disabled>
                    <label for="${result["choices"].id}">
                        <input type="text" value="${result["choices"].choice}" class="edit-choice" data-id="${result["choices"].id}">
                    </label>
                    <span class="remove-option" title = "Remove" data-id="${result["choices"].id}">&times;</span>
                </div>
                <div class="choice">
                    <input type = "radio" id = "add-choice" disabled />
                    <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question"].id}"
                    data-type = "${result["question"].question_type}">Add option</label>
                </div>
            </div>
            <div class="choice-option">
                <input type="checkbox" class="required-checkbox" id="${result["question"].id}" data-id="${result["question"].id}">
                <label for="${result["question"].id}" class="required">Required</label>
                <div class="float-right">
                    <img src="/static/Icon/dustbin.png" alt="Delete question icon" class="question-option-icon delete-question" title="Delete question"
                    data-id="${result["question"].id}">
                </div>
            </div>
            `;
            document.querySelector(".container").appendChild(ele);
            editChoice()
            removeOption()
            changeType()
            editQuestion()
            editRequire()
            addOption()
            deleteQuestion()
        })
    })