async function fetchTestCases() {
    const response = await fetch('/test_cases');
    if (!response.ok) {
        document.getElementById('output').textContent = "Failed to fetch test cases.";
        return;
    }
    const testFiles = await response.json();
    const testFileList = document.getElementById('test-files');
    testFileList.innerHTML = '';
    testFiles.forEach(testFile => {
        const fileDiv = document.createElement('div');
        const fileName = document.createElement('h3');
        fileName.textContent = testFile.file;
        fileDiv.appendChild(fileName);

        const caseList = document.createElement('ul');
        testFile.cases.forEach(testCase => {
            const li = document.createElement('li');
            li.textContent = testCase.name;
            li.dataset.file = testCase.file;
            li.onclick = () => selectTestCase(li);
            caseList.appendChild(li);
        });
        fileDiv.appendChild(caseList);
        testFileList.appendChild(fileDiv);
    });
}

function selectTestCase(li) {
    li.classList.toggle('selected');
}

async function runTests() {
    const selectedTestCases = Array.from(document.querySelectorAll('.selected')).map(li => ({
        file: li.dataset.file,
        name: li.textContent
    }));
    if (selectedTestCases.length === 0) {
        document.getElementById('output').textContent = "No test cases selected.";
        return;
    }
    const response = await fetch('/run_tests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedTestCases)
    });
    const result = await response.json();
    document.getElementById('output').textContent = result.output;
}

window.onload = fetchTestCases;
