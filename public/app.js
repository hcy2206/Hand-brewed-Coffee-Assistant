const coffeeWeightInput = document.getElementById('coffee-weight');
const ratioSelect = document.getElementById('ratio');
const calculateBtn = document.getElementById('calculate-btn');
const resultDiv = document.getElementById('result');
const totalWaterSpan = document.getElementById('total-water');
const stagesList = document.getElementById('stages-list');

calculateBtn.addEventListener('click', async () => {
    const coffeeWeight = parseFloat(coffeeWeightInput.value);
    const ratio = parseFloat(ratioSelect.value);

    if (!coffeeWeight || coffeeWeight <= 0) {
        alert('请输入有效的咖啡粉重量');
        return;
    }

    calculateBtn.disabled = true;
    calculateBtn.textContent = '计算中...';

    try {
        const apiUrl = location.port === '3000' ? 'http://localhost:8000/api/calculate' : '/api/calculate';
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ coffee_weight: coffeeWeight, ratio: ratio })
        });

        if (!response.ok) {
            throw new Error('计算失败');
        }

        const data = await response.json();
        displayResult(data);
    } catch (error) {
        alert('计算出错：' + error.message);
    } finally {
        calculateBtn.disabled = false;
        calculateBtn.textContent = '计算';
    }
});

function displayResult(data) {
    totalWaterSpan.textContent = data.total_water;

    stagesList.innerHTML = data.stages.map(stage => `
        <li>
            <div class="stage-header">
                <span class="stage-name">${stage.name}</span>
                <span class="stage-time">${stage.time}</span>
            </div>
            <div class="stage-water">注水 ${stage.water_amount}g → 累计 ${stage.cumulative_water}g</div>
            <div class="stage-instruction">${stage.instruction}</div>
        </li>
    `).join('');

    resultDiv.classList.remove('hidden');
}
