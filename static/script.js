/*
Get all JSON data for the prediction into an object.
*/
const get_JSON_data=function()
{
	let g=$('select[name="gender"]').val();
	return{
		//Get the gender.
		gender:g,
		//Get the age.
		age:validateAge(),
		//Pregnancies.
		pregnancies:validatePregnancies(g),
		//Glucose level.
		glucose:($('input[name="glucose"]').val()),
		//Blood pressure.
		bp:($('input[name="bp"]').val()),
		//Skin Thickness.
		skin:($('input[name="skin"]').val()),
		//Insulin.
		insulin:($('input[name="insulin"]').val()),
		//BMI.
		bmi:($('input[name="bmi"]').val()),
		//Diabetes Pedigree Function.
		dpf:($('input[name="dpf"]').val()),
	};
}

const validateAge=function()
{
	let age=Number($('input[name="age"]').val());
	if(age>0 && age!=='' && age!==NaN)
		return age;
	$("span#error").text("Valid age is required");
	throw new Error();
}

const validatePregnancies=function(gender)
{
	let p=$('input[name="pregnancies"]').val();
	if(Number(gender)===0 && Number(p)!==0)
	{
		$("span#error").text("Pregnancy count is 0 for males.");
		throw new Error();
	}
	return p;
}

const predict_button_click=function()
{
	//Empty visuals.
	$("span#prediction").text('?');
	$("span#error").text('');

	//Extract data.
	const data=get_JSON_data();
	$("span#status").text('Please wait...');

	//Send data to the backend.
	$.getJSON
	(
		//'dummy_prediction' is the route the data is sent to for processing.
		//The data will be processed by the function at that route.
		//The processed data will be returned as a response.
		$SCRIPT_ROOT + '/predict',
		//All the data extracted so far.
		data,
		//The function callback to execute when the response is received.
		function(response)
		{
			//'prediction' is the key which came in the response which was set in the .py file.
			$("span#status").text('');
			$("span#prediction").text(`Chance of risk:${response.prediction}`);
		}
	);
	return false;
}


const bind_all_functions=function()
{
	//Bind function to button to execute on click.
	$('button#predict').bind('click',predict_button_click);
}

/*
Execute this when the document loads.
*/
$(bind_all_functions);

