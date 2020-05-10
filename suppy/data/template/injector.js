data = JSON.parse(data)
$('#project-name').text(data['project_name'])
var currentdate = new Date(); 
var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
$('#time').text(datetime)

grouped = get_grouped_data(data)

start_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Resources Not Used',
        selector: x => x.not_used_resources
    },
    {
        name: 'Initial Resources Count',
        selector: x => x.resource_count
    },
    {
        name: 'Resource Type',
        selector: x => x.resource_type
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

start_table = get_table_html(grouped['start'], start_table_definition)
$('#start-table').html(start_table)


transport_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Idle Time',
        selector: x => msToTime(x.idle_time)
    },
    {
        name: 'Active Time',
        selector: x => msToTime(x.active_time)
    },
    {
        name: 'Total Cost',
        selector: x => x.total_cost
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

transport_table = get_table_html(grouped['transport'], transport_table_definition)
$('#transport-table').html(transport_table)

transform_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Idle Time',
        selector: x => msToTime(x.idle_time)
    },
    {
        name: 'Active Time',
        selector: x => msToTime(x.active_time)
    },
    {
        name: 'Calibration Time',
        selector: x => msToTime(x.calibration_time)
    },
    {
        name: 'Active Cost',
        selector: x => x.total_cost
    },
    {
        name: 'Calibration Cost',
        selector: x => x.total_calibration_cost
    },
    {
        name: 'Calibration Count',
        selector: x => x.calibration_count
    },
    {
        name: 'Calibration Steps Left',
        selector: x => x.calibration_left
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

transform_table_definition = get_table_html(grouped['custom'], transform_table_definition)
$('#transform-table').html(transform_table_definition)

buffer_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Max Capacity',
        selector: x => x.capacity
    },
    {
        name: 'Capacity Reached',
        selector: x => x.was_full ? 'Yes': 'No'
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

buffer_table = get_table_html(grouped['buffer'], buffer_table_definition)
$('#buffer-table').html(buffer_table)

convergence_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Flow count',
        selector: x => x.runs
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

convergence_table = get_table_html(grouped['convergence'], convergence_table_definition)
$('#convergence-table').html(convergence_table)

divergence_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Flow count',
        selector: x => x.runs
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

divergence_table = get_table_html(grouped['DIVERGENCE'], divergence_table_definition)
$('#divergence-table').html(divergence_table)

test_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Idle Time',
        selector: x => msToTime(x.idle_time)
    },
    {
        name: 'Active Time',
        selector: x => msToTime(x.active_time)
    },
    {
        name: 'Calibration Time',
        selector: x => msToTime(x.calibration_time)
    },
    {
        name: 'Active Cost',
        selector: x => x.total_cost
    },
    {
        name: 'Calibration Cost',
        selector: x => x.total_calibration_cost
    },
    {
        name: 'Calibration Count',
        selector: x => x.calibration_count
    },
    {
        name: 'Calibration Steps Left',
        selector: x => x.calibration_left
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    },
    {
        name: 'Runs',
        selector: x => x.runs
    },
    {
        name: 'Errors Missed',
        selector: x => x.errors_missed
    },
    {
        name: 'Errors Found',
        selector: x => x.errors_found
    }
]

test_table = get_table_html(grouped['test'], test_table_definition)
$('#test-table').html(test_table)

repair_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Idle Time',
        selector: x => msToTime(x.idle_time)
    },
    {
        name: 'Active Time',
        selector: x => msToTime(x.active_time)
    },
    {
        name: 'Calibration Time',
        selector: x => msToTime(x.calibration_time)
    },
    {
        name: 'Active Cost',
        selector: x => x.total_cost
    },
    {
        name: 'Calibration Cost',
        selector: x => x.total_calibration_cost
    },
    {
        name: 'Calibration Count',
        selector: x => x.calibration_count
    },
    {
        name: 'Calibration Steps Left',
        selector: x => x.calibration_left
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    },
    {
        name: 'Repairs',
        selector: x => x.repairs
    },
    {
        name: 'Non Repairs',
        selector: x => x.non_repairs
    }
]

repair_table = get_table_html(grouped['repair'], repair_table_definition)
$('#repair-table').html(repair_table)

error_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Semi Finite Count',
        selector: x => x.semi_finite.length
    }
]

error_table = get_table_html(grouped['random_error'], error_table_definition)
$('#error-table').html(error_table)

end_table_definition = [
    {
        name: 'Name',
        selector: x => x.name
    },
    {
        name: 'Resource Count',
        selector: x => x.resource_count
    },
    {
        name: 'Valid Resource Count',
        selector: x => x.valid_resource_count
    },
    {
        name: 'Products',
        selector: x =>  parseObjectTypesAndCount(parseWarehoseItems(x))
    },
    {
        name: 'Errors',
        selector: x =>  parseErrorsAndCount(x.errors) 
    }
]

function parseObjectTypesAndCount(data) {
    values = []
    for (const [key, value] of Object.entries(data)) {
        values.push(key + ':' + value.count);
    }
    return values.join(', ');
}

function parseErrorsAndCount(data) {
    values = [];
    for (const [key, value] of Object.entries(data)) {
        values.push(key + ':' + value);
    }
    if (!values.length){
        return '0';
    }
    return values.join(', ');
}

end_table = get_table_html(grouped['end'], end_table_definition)
$('#end-table').html(end_table)




cost = get_cost(data.stats)




var ctx = document.getElementById('cost').getContext('2d');
var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            data: [
                cost.transport_cost,
                cost.transform_cost + cost.transform_calibration_cost,
                cost.verification_cost + cost.verification_calibration_cost,
                cost.repair_cost + cost.repair_calibration_cost,
            ],
            backgroundColor: [
                '#4dc9f6',
                '#f67019',
                '#f53794',
                '#537bc4',
                '#acc236',
                '#166a8f',
                '#00a950',
                '#58595b',
                '#8549ba'
            ]
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Transport',
            'Transform',
            'Verification',
            'Repairs'
        ]
    }
});

var ctx = document.getElementById('cost-detail').getContext('2d');
var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            data: [
                cost.transport_cost,
                cost.transform_cost,
                cost.transform_calibration_cost,
                cost.verification_cost,
                cost.verification_calibration_cost,
                cost.repair_cost,
                cost.repair_calibration_cost
            ],
            backgroundColor: [
                '#4dc9f6',
                '#f67019',
                '#f53794',
                '#537bc4',
                '#acc236',
                '#166a8f',
                '#00a950',
                '#58595b',
                '#8549ba'
            ]
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Transport',
            'Transform Active',
            'Transform Calibration',
            'Verification',
            'Verification Calibration',
            'Repair',
            'Repair Calibration'
        ]
    }
});

var total_cost = cost.transport_cost +
cost.transform_cost +
cost.transform_calibration_cost +
cost.verification_cost +
cost.verification_calibration_cost +
cost.repair_cost +
cost.repair_calibration_cost

$('#total-cost').text(total_cost)
$('#duration').text(msToTime(data.time))