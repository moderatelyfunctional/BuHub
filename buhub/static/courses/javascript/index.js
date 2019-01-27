$(document).ready(function() {
	$('.major-item').on('click', select_major);
	$('.ap-item').on('click', select_ap);
	$('#submit-major-btn').on('click', show_ap_classes);
	$('#submit-ap-btn').on('click', show_hub_classes);
	$('#submit-hub-btn').on('click', ajaxFetchHubClasses);
});

let curr_selected;
const select_major = function() {
	if (curr_selected) {
		curr_selected.removeClass('selected-major-item');
	}
	$(this).addClass('selected-major-item');
	curr_selected = $(this);
}

const show_ap_classes = function() {
	$('#submit-major-container').addClass('hide');
	$('#submit-ap-container').removeClass('hide');
}

let curr_selected_aps = [];
let other = {
	'4': '5',
	'5': '4',
};
const select_ap = function() {
	const selected_class = 'selected-major-item';
	const hyphen_index = $(this).attr('id').indexOf('-');
	const exam_name = $(this).attr('id').slice(0, hyphen_index);
	const score = $(this).attr('id').slice(hyphen_index + 1);

	const other_exam = exam_name + '-' + other[score];

	if ($(this).hasClass(selected_class)) {
		$(this).removeClass(selected_class);
		const remove_index = curr_selected_aps.indexOf($(this).attr('id'));
		curr_selected_aps.splice(remove_index, 1);

	} else {
		$(this).addClass(selected_class);
		curr_selected_aps.push($(this).attr('id'));

		if (curr_selected_aps.indexOf(other_exam) >= 0) {
			$('#' + other_exam).removeClass(selected_class);
			const other_remove_index = curr_selected_aps.indexOf(other_exam);
			curr_selected_aps.splice(other_remove_index, 1);
		}
	}
}

const min_zero = function(n) {
	if (n < 0) {
		return 0;
	}
	return n;
}

let subarea_to_units = {
	'PILM': 1,
	'AE': 1,
	'HC': 1,
	'SCI I': 1,
	'SOC I': 1,
	'SCI-IISOC-II': 1,
	'QR I': 1,
	'QR II': 1,
	'IC': 1,
	'GCIL': 2,
	'ER': 1,
	'FYWS': 1,
	'WRI': 1,
	'WIC': 2,
	'OSC': 1,
	'DME': 1,
	'CT': 2,
	'RIL': 2,
	'TC': 2,
	'CI': 2
}

const show_hub_classes = function() {
	for (let i = 0; i < curr_selected_aps.length; i++) {
		const key = curr_selected_aps[i];
		const subarea_key = ap_to_hub[key];
		if (subarea_key == 'SCI I,SCI II') {
			subarea_to_units['SCI-IISOC-II'] -= 1;
			subarea_to_units['SCI I'] -= 1;			
		}
		else if (subarea_key == 'SOC-II' || subarea_key == 'SCI-II') {
			subarea_to_units['SCI-IISOC-II'] -= 1;
		} else {
			subarea_to_units[subarea_key] -= 1; 
		}
	}

	for (let subarea_key in subarea_to_units) {
		const curr_units = subarea_to_units[subarea_key]

		let identifier = subarea_key;
		const space_index = subarea_key.indexOf(' ');
		if (space_index >= 0) {
			const before = subarea_key.slice(0, space_index);
			const after = subarea_key.slice(space_index + 1);			
			identifier = before + '-' + after;
		}

		$('#' + identifier).text(min_zero(curr_units));
	}

	$('#submit-ap-container').addClass('hide');
	$('#submit-hub-container').removeClass('hide');
}

const ajaxFetchHubClasses = function() {
	$.ajax({
		url: '/fetch_hub_classes/',
		type: 'post',
		data: {units_left: subarea_to_units},
		success: function(data) {
			const parsed_data = JSON.parse(data)['hub_classes'];
			for (let i = 0; i < parsed_data.length; i++) {
				const class_name = parsed_data[i];
				const first_b = class_name.indexOf('b');
				const before_b = class_name.slice(0, first_b);
				const after_b = class_name.slice(first_b + 1);

				const class_div = $('<div>', {
					'text': before_b + after_b,
					'class': 'hub-class'
				})
				$('#hub-classes').append(class_div)
			}
		},
		error: function(err) {
			console.log(err);
		}
	})
}








