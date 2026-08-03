redirectIfNotLoggedIn();

window.onload = function () {

    loadMonthlyRevenue();

    loadSubscriptionSummary();

    loadPlanDistribution();

};

// ======================================
// Monthly Revenue
// ======================================

async function loadMonthlyRevenue() {

    const response = await fetch(

        `${API_BASE_URL}/reports/monthly-revenue`,

        {

            headers: authHeaders()

        }

    );

    const report = await response.json();

    document.getElementById(

        "monthlyRevenue"

    ).innerHTML = `

        <p>

            <strong>Month:</strong>

            ${report.month}

        </p>

        <p>

            <strong>Total Subscriptions:</strong>

            ${report.total_subscriptions}

        </p>

        <p>

            <strong>Revenue:</strong>

            ₹${report.estimated_revenue}

        </p>

    `;

}

// ======================================
// Subscription Summary
// ======================================

async function loadSubscriptionSummary() {

    const response = await fetch(

        `${API_BASE_URL}/reports/subscription-summary`,

        {

            headers: authHeaders()

        }

    );

    const summary = await response.json();

    document.getElementById(

        "subscriptionSummary"

    ).innerHTML = `

        <p>

            <strong>Active:</strong>

            ${summary.active_subscriptions}

        </p>

        <p>

            <strong>Cancelled:</strong>

            ${summary.cancelled_subscriptions}

        </p>

    `;

}

// ======================================
// Plan Distribution
// ======================================

async function loadPlanDistribution() {

    const response = await fetch(

        `${API_BASE_URL}/reports/plan-distribution`,

        {

            headers: authHeaders()

        }

    );

    const plans = await response.json();

    let html = "";

    plans.forEach(plan => {

        html += `

            <p>

                <strong>${plan.plan_name}</strong>

                : ${plan.total_subscriptions}

            </p>

        `;

    });

    document.getElementById(

        "planDistribution"

    ).innerHTML = html;

}

// ======================================
// Downloads
// ======================================

function downloadCSV() {

    window.open(

        `${API_BASE_URL}/reports/export/csv/monthly-revenue`,

        "_blank"

    );

}

function downloadPDF() {

    window.open(

        `${API_BASE_URL}/reports/export/pdf/monthly-revenue`,

        "_blank"

    );

}