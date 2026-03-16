// ── Custom number controls ──

document.querySelectorAll("input[type=number]").forEach(input => {
    const wrap = document.createElement("span");
    wrap.className = "num-control";

    const btnDec = document.createElement("button");
    btnDec.type = "button";
    btnDec.className = "num-btn";
    btnDec.textContent = "\u2212";
    btnDec.setAttribute("aria-label", "Decrease");

    const btnInc = document.createElement("button");
    btnInc.type = "button";
    btnInc.className = "num-btn";
    btnInc.textContent = "+";
    btnInc.setAttribute("aria-label", "Increase");

    input.parentElement.insertBefore(wrap, input);
    wrap.appendChild(btnDec);
    wrap.appendChild(input);
    wrap.appendChild(btnInc);

    btnDec.addEventListener("click", () => {
        const min = Number(input.min);
        const val = Number(input.value) - 1;
        input.value = Math.max(min, val);
    });

    btnInc.addEventListener("click", () => {
        const max = Number(input.max);
        const val = Number(input.value) + 1;
        input.value = Math.min(max, val);
    });
});

// ── Validation ──

function clearErrors(form) {
    form.querySelectorAll(".error-tooltip").forEach(el => el.remove());
    form.querySelectorAll(".input-error").forEach(el => el.classList.remove("input-error"));
    form.querySelectorAll(".input-wrap").forEach(wrap => {
        const control = wrap.querySelector(".num-control");
        wrap.replaceWith(control);
    });
}

function showTooltip(input, text) {
    const control = input.closest(".num-control");
    const wrap = document.createElement("span");
    wrap.className = "input-wrap";
    control.parentElement.insertBefore(wrap, control);
    wrap.appendChild(control);

    const tip = document.createElement("span");
    tip.className = "error-tooltip";
    tip.textContent = text;
    wrap.appendChild(tip);

    setTimeout(() => {
        tip.classList.add("fade-out");
        tip.addEventListener("animationend", () => tip.remove());
    }, 10000);
}

function validateForm(form) {
    let valid = true;
    clearErrors(form);

    form.querySelectorAll("input[type=number]").forEach(input => {
        const val = Number(input.value);
        const min = Number(input.min);
        const max = Number(input.max);

        if (input.value === "" || val < min || val > max) {
            valid = false;
            input.closest(".num-control").classList.add("input-error");
            showTooltip(input, `Value must be between ${min} and ${max}`);
        }
    });

    return valid;
}

// ── Form submission ──

document.getElementById("predict-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;

    if (!validateForm(form)) return;

    const formData = new FormData(form);

    const data = {
        hit_points: Number(formData.get("hit_points")),
        armor_class: Number(formData.get("armor_class")),
        strength: Number(formData.get("strength")),
        dexterity: Number(formData.get("dexterity")),
        constitution: Number(formData.get("constitution")),
        intelligence: Number(formData.get("intelligence")),
        wisdom: Number(formData.get("wisdom")),
        charisma: Number(formData.get("charisma")),
        num_actions: Number(formData.get("num_actions")),
        num_resistances: Number(formData.get("num_resistances")),
        num_immunities: Number(formData.get("num_special_abilities")),
        num_special_abilities: Number(formData.get("num_special_abilities")),
        has_legendary_actions: form.querySelector("[name=has_legendary_actions]").checked,
        has_spellcasting: form.querySelector("[name=has_spellcasting]").checked,
    };

    const response = await fetch("/api/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data),
    });

    const result = await response.json();

    document.getElementById("cr-value").textContent = result.predicted_cr.toFixed(1);
    document.getElementById("modal-overlay").classList.add("visible");
});

// ── Modal ──

document.getElementById("modal-close").addEventListener("click", () => {
    document.getElementById("modal-overlay").classList.remove("visible");
});

document.getElementById("modal-overlay").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) {
        document.getElementById("modal-overlay").classList.remove("visible");
    }
});

// ── Randomize ──

function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.getElementById("randomize").addEventListener("click", () => {
    const form = document.getElementById("predict-form");

    form.querySelector("[name=hit_points]").value = randInt(1, 1000);
    form.querySelector("[name=armor_class]").value = randInt(5, 30);
    form.querySelector("[name=strength]").value = randInt(1, 30);
    form.querySelector("[name=dexterity]").value = randInt(1, 30);
    form.querySelector("[name=constitution]").value = randInt(1, 30);
    form.querySelector("[name=intelligence]").value = randInt(1, 30);
    form.querySelector("[name=wisdom]").value = randInt(1, 30);
    form.querySelector("[name=charisma]").value = randInt(1, 30);
    form.querySelector("[name=num_actions]").value = randInt(0, 10);
    form.querySelector("[name=num_resistances]").value = randInt(0, 10);
    form.querySelector("[name=num_immunities]").value = randInt(0, 10);
    form.querySelector("[name=num_special_abilities]").value = randInt(0, 10);
    form.querySelector("[name=has_legendary_actions]").checked = Math.random() < 0.15;
    form.querySelector("[name=has_spellcasting]").checked = Math.random() < 0.2;
});
