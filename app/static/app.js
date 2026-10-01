const API = "/api";


let token =
    localStorage.getItem(
        "pocketsmart_token"
    );


// ======================================================
// HELPER
// ======================================================

const $ = (selector) =>
    document.querySelector(selector);


function formDataObject(form) {

    return Object.fromEntries(
        new FormData(form).entries()
    );
}


// ======================================================
// API
// ======================================================

async function api(
    path,
    options = {}
) {

    options.headers =
        options.headers || {};


    if (token) {

        options.headers.Authorization =
            `Bearer ${token}`;
    }


    const response =
        await fetch(
            API + path,
            options
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );
    }


    return data;
}


// ======================================================
// LOGIN UI
// ======================================================

function showLoggedIn() {

    $("#auth")
        .classList
        .add("hidden");


    $("#planner")
        .classList
        .remove("hidden");


    $("#userNav").innerHTML = `
        <button onclick="logout()">
            Logout
        </button>
    `;
}


// ======================================================
// LOGIN / REGISTER
// ======================================================

async function loginOrRegister(
    url,
    form
) {

    try {

        const response =
            await api(
                url,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        formDataObject(form)
                    )
                }
            );


        token =
            response.access_token;


        localStorage.setItem(
            "pocketsmart_token",
            token
        );


        showLoggedIn();


    } catch (error) {

        alert(error.message);
    }
}


// ======================================================
// REGISTER
// ======================================================

$("#registerForm")
    .addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            loginOrRegister(
                "/register",
                event.target
            );
        }
    );


// ======================================================
// LOGIN
// ======================================================

$("#loginForm")
    .addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            loginOrRegister(
                "/login",
                event.target
            );
        }
    );


// ======================================================
// LOGOUT
// ======================================================

window.logout = function () {

    token = null;

    localStorage.removeItem(
        "pocketsmart_token"
    );

    location.reload();
};


// ======================================================
// TABS
// ======================================================

document
    .querySelectorAll(
        ".tabs button"
    )
    .forEach(
        (button) => {

            button.onclick = () => {

                document
                    .querySelectorAll(
                        ".tab"
                    )
                    .forEach(
                        (section) => {

                            section
                                .classList
                                .add(
                                    "hidden"
                                );
                        }
                    );


                const tab =
                    button.dataset.tab;


                $("#" + tab)
                    .classList
                    .remove(
                        "hidden"
                    );


                if (
                    tab === "history"
                ) {

                    loadHistory();
                }
            };
        }
    );


// ======================================================
// RENDER RESULT
// ======================================================

function renderResult(data) {


    const allocations =
        (data.allocation || [])
            .map(
                (allocation) => `

                    <div>

                        <b>
                            ${allocation.category}
                        </b>

                        <br>

                        ₹${Number(
                            allocation.amount
                        ).toLocaleString("en-IN")}

                    </div>

                `
            )
            .join("");


    const recommendations =
        (data.recommendations || [])
            .map(
                (recommendation) => `

                    <div class="rec">

                        <h3>
                            ${recommendation.name}
                        </h3>


                        <b>
                            ₹${Number(
                                recommendation.estimated_price || 0
                            ).toLocaleString("en-IN")}
                        </b>


                        <p>
                            ${recommendation.reason}
                        </p>


                        <small>
                            ${recommendation.platform || ""}
                        </small>


                        <br>


                        <a
                            href="${recommendation.search_url}"
                            target="_blank"
                            rel="noopener"
                        >

                            Search on
                            ${recommendation.platform}
                            →

                        </a>

                    </div>

                `
            )
            .join("");


    $("#result").innerHTML = `

        <div class="result-card">

            <div class="status">

                AI mode:
                ${data.source_mode}

            </div>


            <h2>
                ${data.title}
            </h2>


            <p>
                ${data.summary}
            </p>


            <h3>
                Budget Allocation
            </h3>


            <div class="alloc">

                ${allocations}

            </div>


            <h3>
                Recommendations
            </h3>


            <div class="recommendations">

                ${recommendations}

            </div>

        </div>

    `;
}


// ======================================================
// JSON REQUEST
// ======================================================

async function sendJSON(
    path,
    form
) {

    $("#result").innerHTML = `
        <div class="panel">
            Generating your plan...
        </div>
    `;


    try {

        let data =
            formDataObject(form);


        // Convert numeric values

        if (data.budget) {

            data.budget =
                Number(data.budget);
        }


        if (data.guests) {

            data.guests =
                Number(data.guests);
        }


        // Convert comma-separated lists

        if (path === "/generate-home") {

            data.rooms =
                data.rooms
                    .split(",")
                    .map(
                        value =>
                            value.trim()
                    )
                    .filter(Boolean);


            data.items =
                data.items
                    .split(",")
                    .map(
                        value =>
                            value.trim()
                    )
                    .filter(Boolean);
        }


        const response =
            await api(
                path,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        renderResult(response);


    } catch (error) {

        $("#result").innerHTML = `

            <div class="panel">

                ${error.message}

            </div>

        `;
    }
}


// ======================================================
// HOME
// ======================================================

$("#homeForm")
    .addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            sendJSON(
                "/generate-home",
                event.target
            );
        }
    );


// ======================================================
// PARTY
// ======================================================

$("#partyForm")
    .addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            sendJSON(
                "/generate-party",
                event.target
            );
        }
    );


// ======================================================
// JEWELRY
// ======================================================

$("#jewelryForm")
    .addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            $("#result").innerHTML = `

                <div class="panel">

                    Analyzing your jewelry plan...

                </div>

            `;


            try {

                const formData =
                    new FormData(
                        event.target
                    );


                formData.set(
                    "budget",
                    Number(
                        formData.get(
                            "budget"
                        )
                    )
                );


                const response =
                    await api(
                        "/generate-jewelry",
                        {

                            method: "POST",

                            body: formData

                        }
                    );


                renderResult(
                    response
                );


            } catch (error) {

                $("#result").innerHTML = `

                    <div class="panel">

                        ${error.message}

                    </div>

                `;
            }
        }
    );


// ======================================================
// HISTORY
// ======================================================

async function loadHistory() {

    try {

        const rows =
            await api(
                "/history"
            );


        if (!rows.length) {

            $("#historyList").innerHTML =
                "<p>No saved plans yet.</p>";

            return;
        }


        $("#historyList").innerHTML =
            rows
                .map(
                    (row) => `

                        <div class="rec">

                            <b>
                                ${row.planner.toUpperCase()}
                            </b>

                            —

                            ${row.created_at}


                            <p>
                                ${row.response.summary}
                            </p>

                        </div>

                    `
                )
                .join("");


    } catch (error) {

        $("#historyList").innerHTML =
            error.message;
    }
}


// ======================================================
// AUTO LOGIN
// ======================================================

if (token) {

    showLoggedIn();
}