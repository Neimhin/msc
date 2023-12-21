export function injury_to_broad_injury(incident) {
    switch (incident) {
        case "gunfire":
            return "gunfire";
        case "explosion":
        case "shelling":
            return "explosive";
        case "stabbing":
        case "stones throwing":
        case "hit by a vehicle":
        case "beating":
        case "being bludgeoned with an axe":
        case "Strangulation":
        case "physically assaulted":
        case "physical assault":
            return "assault";
        case "house demolition":
        case "fire":
            return "fire/demolition";
        default:
            return "fire/demolition";
    }
}
export function broad_injury_to_injuries(category) {
    switch (category) {
        case "gunfire":
            return ["gunfire"];
        case "explosive":
            return ["explosion", "shelling"];
        case "assault":
            return ["stabbing", "stones throwing", "hit by a vehicle", "beating", "being bludgeoned with an axe", "Strangulation", "physically assaulted", "physical assault"];
        case "fire/demolition":
            return ["house demolition", "fire"];
        default:
            return [];
    }
}
export function flatten_and_count_injuries(bins) {
    let counts = {
        "gunfire": 0,
        "assault": 0,
        "explosive": 0,
        "fire/demolition": 0,
    };
    bins.forEach(bin => {
        bin.forEach((item) => {
            const category = item.broad_injury;
            counts[category] = (counts[category] || 0) + 1;
        });
    });
    return Object.keys(counts).map(key => ({ category: key, value: counts[key] }));
}
export function flatten_and_count_man_woman_child(bins) {
    let counts = {
        "palestinian man": 0,
        "palestinian woman": 0,
        "palestinian minor": 0,
        "israeli man": 0,
        "israeli woman": 0,
        "israeli minor": 0,
    };
    function categorise(d) {
        let str;
        if (d.citizenship === "Palestinian") {
            str = "palestinian ";
        }
        else if (d.citizenship === "Israeli") {
            str = "israeli ";
        }
        else {
            return null;
        }
        if (d.age < 18)
            return str + "minor";
        const g = d.gender === "M" ? "man" : "woman";
        return str + g;
    }
    bins.forEach(bin => {
        bin.forEach((item) => {
            const category = categorise(item);
            if (category) {
                counts[category] = (counts[category] || 0) + 1;
            }
        });
    });
    return Object.keys(counts).map(key => ({ category: key, value: counts[key] }));
}
export function flatten_and_perpetrator(bins) {
    let counts = {
        "Israeli civilians": 0,
        "Palestinian civilians": 0,
        "Israeli security forces": 0,
    };
    function categorise(d) {
        return "" + d.killed_by;
    }
    bins.forEach(bin => {
        bin.forEach((item) => {
            const category = categorise(item);
            if (category) {
                counts[category] = (counts[category] || 0) + 1;
            }
        });
    });
    return Object.keys(counts).map(key => ({ category: key, value: counts[key] }));
}
//# sourceMappingURL=pure.js.map