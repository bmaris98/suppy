function get_grouped_data(input) {
    grouped = {
        'custom': [],
        'start': [],
        'end': [],
        'random_error': [],
        'transport': [],
        'repair': [],
        'test': [],
        'buffer': [],
        'convergence': [],
        'DIVERGENCE': []
    }

    input.stats.forEach(element => {
        grouped[element.type].push(element)
    });

    return grouped
}

function msToTime(s) {
    var ms = s % 1000;
    s = (s - ms) / 1000;
    var secs = s % 60;
    s = (s - secs) / 60;
    var mins = s % 60;
    var hrs = (s - mins) / 60;
  
    return hrs + ':' + mins + ':' + secs + '.' + ms;
}

function parseWarehoseItems(warehouse) {
    stat = {};
    warehouse.resources.forEach(resource => {
        if (resource._category in stat) {
            stat[resource._category].count++;
            resource._errors.forEach(error => {
                stat[resource._category].errors.push(error);
            });
        } else {
            stat[resource._category] = {}
            stat[resource._category].count = 1;
            stat[resource._category].errors = [];
        }
    });
    final = {}
    for (const [key, value] of Object.entries(stat)) {
        final[key] = {
            count: value.count,
            errors: value.errors.reduce((a, c) => (a[c] = (a[c] || 0) + 1, a), Object.create(null))
        };
    }
    return final;
}

function get_cost(data) {
    var transport_cost = 0;
    var transform_cost = 0;
    var transform_calibration_cost = 0;
    var verification_cost = 0;
    var verification_calibration_cost = 0;
    var repair_cost = 0;
    var repair_calibration_cost = 0;
    data.forEach(stat => {
        if (stat.type == 'custom') {
            transform_cost += stat.total_cost;
            transform_calibration_cost += stat.total_calibration_cost;
        }
        else if (stat.type == 'transport') {
            transport_cost += stat.total_cost;
        }
        else if (stat.type == 'test') {
            verification_cost += stat.total_cost;
            verification_calibration_cost += stat.total_calibration_cost;
        }
        else if (stat.type == 'repair') {
            repair_cost += stat.total_cost;
            repair_calibration_cost += stat.total_calibration_cost;
        }
    }, this);

    return {
        transport_cost: transport_cost,
        transform_cost: transform_cost,
        transform_calibration_cost: transform_calibration_cost,
        verification_cost: verification_cost,
        verification_calibration_cost: verification_calibration_cost,
        repair_cost: repair_cost,
        repair_calibration_cost: repair_calibration_cost
    };
}