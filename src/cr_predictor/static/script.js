document.getElementById("predict-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
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
        num_immunities: Number(formData.get("num_immunities")),
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

document.getElementById("modal-close").addEventListener("click", () => {
    document.getElementById("modal-overlay").classList.remove("visible");
});

document.getElementById("modal-overlay").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) {
        document.getElementById("modal-overlay").classList.remove("visible");
    }
});

function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.getElementById("randomize").addEventListener("click", () => {
    const form = document.getElementById("predict-form");

    form.querySelector("[name=hit_points]").value = randInt(1, 676);
    form.querySelector("[name=armor_class]").value = randInt(5, 25);
    form.querySelector("[name=strength]").value = randInt(1, 30);
    form.querySelector("[name=dexterity]").value = randInt(1, 28);
    form.querySelector("[name=constitution]").value = randInt(8, 30);
    form.querySelector("[name=intelligence]").value = randInt(1, 25);
    form.querySelector("[name=wisdom]").value = randInt(3, 25);
    form.querySelector("[name=charisma]").value = randInt(1, 30);
    form.querySelector("[name=num_actions]").value = randInt(0, 7);
    form.querySelector("[name=num_resistances]").value = randInt(0, 6);
    form.querySelector("[name=num_immunities]").value = randInt(0, 4);
    form.querySelector("[name=num_special_abilities]").value = randInt(0, 6);
    form.querySelector("[name=has_legendary_actions]").checked = Math.random() < 0.15;
    form.querySelector("[name=has_spellcasting]").checked = Math.random() < 0.2;
});
