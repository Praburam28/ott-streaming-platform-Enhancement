redirectIfNotLoggedIn();
loadCurrentSubscription();

loadPlans();
let selectedPlanId = null;
let retryPlanId = null;
async function loadPlans() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/subscription/plans`
        );

        if (!response.ok) {
            throw new Error("Failed to load subscription plans.");
        }

        const plans = await response.json();

        renderPlans(plans);

    } catch (error) {

        console.error(error);

    }

}

function getFeatures(planName) {

    switch ((planName || "").toLowerCase()) {

        case "free":

            return [
                "✔ SD Streaming",
                "✔ 1 Device",
                "✔ Limited Movies",
                "✔ Music Streaming",
                "✖ Offline Download",
                "✖ 4K Ultra HD"
            ];

        case "basic":

            return [
                "✔ Full HD Streaming",
                "✔ 2 Devices",
                "✔ Movies & Series",
                "✔ Music Streaming",
                "✔ No Ads",
                "✖ 4K Ultra HD"
            ];

        case "premium":

            return [
                "✔ 4K Ultra HD",
                "✔ 4 Devices",
                "✔ Unlimited Movies",
                "✔ Unlimited Series",
                "✔ Unlimited Music",
                "✔ Offline Download"
            ];

        default:

            return [
                "✔ Streaming Access"
            ];
    }

}

function renderPlans(plans) {

    const container =
        document.getElementById("plansContainer");

    container.innerHTML = "";

    plans.forEach(plan => {

        // Use whichever field exists
        const planName =
            plan.name ||
            plan.plan_name ||
            plan.title ||
            "Plan";

        const features =
            getFeatures(planName)
                .map(feature => `<li>${feature}</li>`)
                .join("");

        container.innerHTML += `

        <div class="plan-card">

            ${planName.toLowerCase() === "premium"
                ? '<div class="popular">MOST POPULAR</div>'
                : ''}

            <div class="plan-header">

                <h2>${planName}</h2>

                <div class="price">

                    ₹${plan.price}

                </div>

                <div class="days">

                    ${plan.duration_days} Days

                </div>

            </div>

            <ul class="features">

                ${features}

            </ul>

            <button
                class="subscribe-btn"
                onclick="showProrationPreview(
    ${plan.id},
    '${planName}',
    ${plan.price}
)">

                Subscribe

            </button>

        </div>

        `;

    });

}

async function subscribe(planId) {

    try {

        const response = await fetch(

            `${API_BASE_URL}/subscription/subscribe`,

            {

                method: "POST",

                headers: {

                    ...authHeaders(),

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    plan_id: planId

                })

            }

        );

        if (response.ok) {

            alert("🎉 Subscription Activated Successfully!");

            window.location.href = "dashboard.html";

        } else {

            retryPlanId = planId;

            document.getElementById(
            "paymentFailureModal"
            ).style.display = "flex";



        }

    } catch (error) {

    console.error(error);

    retryPlanId = planId;

    document.getElementById(
        "paymentFailureModal"
    ).style.display = "flex";

    }
}


async function loadCurrentSubscription() {

    try {

        const response = await fetch(

            `${API_BASE_URL}/subscription/current`,

            {

                headers: authHeaders()

            }

        );

        if (!response.ok) {

            document.getElementById(
                "currentSubscriptionCard"
            ).innerHTML = `
                <p>No active subscription.</p>
            `;

            return;

        }

        const subscription = await response.json();

if ((subscription.status || "").toUpperCase() === "ACTIVE") {
    
    document.getElementById(
        "currentSubscriptionCard"
    ).innerHTML = `

        <div class="current-plan">

            <h3>
                Plan ID : ${subscription.plan_id}
            </h3>

            <p>
                Status : ${subscription.status}
            </p>

            <p>
                Expiry :
                ${new Date(
                    subscription.end_date
                ).toLocaleDateString()}
            </p>

            <button
                class="cancel-btn"
                onclick="openCancelModal()">

                Cancel Subscription

            </button>

        </div>

    `;

}
else {

    document.getElementById(
        "currentSubscriptionCard"
    ).innerHTML = `

        <div class="current-plan">

            <h3>
                Subscription Expired
            </h3>

            <p>
                Renew your subscription to continue streaming.
            </p>

            <button
                class="subscribe-btn"
                onclick="window.scrollTo({
                    top:600,
                    behavior:'smooth'
                })">

                Renew Subscription

            </button>

        </div>

    `;

}

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "currentSubscriptionCard"
        ).innerHTML = `
            <p>Unable to load subscription.</p>
        `;

    }

}
// ======================================
// Cancel Subscription Modal
// ======================================

function openCancelModal() {

    const modal = document.getElementById("cancelModal");

    if (modal) {
        modal.style.display = "flex";
    }

}

function closeModal() {

    const modal = document.getElementById("cancelModal");

    if (modal) {
        modal.style.display = "none";
    }

}


// ======================================
// Cancel Subscription
// ======================================

async function confirmCancel() {

    try {

        const response = await fetch(

            `${API_BASE_URL}/subscription/cancel`,

            {

                method: "DELETE",

                headers: authHeaders()

            }

        );

        const result = await response.json();

        if (!response.ok) {

            alert(result.detail || "Unable to cancel subscription.");

            return;

        }

        alert(result.message);

        closeModal();

        loadCurrentSubscription();

        loadPlans();

    }

    catch (error) {

    console.error(error);

    document.getElementById(
        "currentSubscriptionCard"
    ).innerHTML = `

        <div class="current-plan">

            <h3>

                Network Error

            </h3>

            <p>

                Unable to connect to the server.

            </p>

            <button
                class="subscribe-btn"
                onclick="loadCurrentSubscription()">

                Retry

            </button>

        </div>

    `;

}

}

// ======================================
// Proration Preview
// ======================================

async function showProrationPreview(
    planId,
    planName,
    planPrice
) {

    selectedPlanId = planId;

    try {

        const response = await fetch(

            `${API_BASE_URL}/subscription/proration-preview`,

            {

                method: "POST",

                headers: {

                    ...authHeaders(),

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    plan_id: planId

                })

            }

        );

        if (!response.ok) {

            // User may not have an active subscription yet.
            // Fall back to the normal subscribe flow.
            subscribe(planId);
            return;

        }

        const preview = await response.json();

        document.getElementById(
            "prorationContent"
        ).innerHTML = `

            <p>

                <strong>Current Plan:</strong>
                ${preview.current_plan}

            </p>

            <p>

                <strong>New Plan:</strong>
                ${preview.new_plan}

            </p>

            <p>

                <strong>Remaining Days:</strong>
                ${preview.remaining_days}

            </p>

            <p>

                <strong>Credit:</strong>

                ₹${preview.credit_amount}

            </p>

            <p>

                <strong>Payable:</strong>

                ₹${preview.payable_amount}

            </p>

        `;

        document.getElementById(
            "prorationModal"
        ).style.display = "flex";

    }

    catch (error) {

        console.error(error);

        subscribe(planId);

    }

}

function closeProrationModal() {

    document.getElementById(
        "prorationModal"
    ).style.display = "none";

}

function confirmProration() {

    closeProrationModal();

    subscribe(selectedPlanId);

}

function closePaymentFailureModal() {

    document.getElementById(
        "paymentFailureModal"
    ).style.display = "none";

}

function retrySubscription() {

    closePaymentFailureModal();

    subscribe(retryPlanId);

}