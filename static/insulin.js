function insulin()
{
	document.getElementById("error").style.border = null;
	document.getElementById("error").innerHTML = null;
	document.getElementById("calculatedDoseBox").innerHTML = null;

	var cbg = document.getElementById("number1").value;
	var meal = document.getElementById("number2").value;
	var Cratio = document.getElementById("number3").value;
	var correction = document.getElementById("number4").value;
	var tbg = document.getElementById("number5").value;

	if(cbg == NaN || cbg < 70 || cbg > 500) 
	{
		document.getElementById("error").innerHTML = "Please enter your current\
		bloodsugar in mg/DL, within the values of 70 and 500";
		document.getElementById("error").style.border = "10px solid red";
		return;
	}
	if(meal == NaN || meal < 1 || meal > 300)
	{
		document.getElementById("error").innerHTML = "Please enter the amount of\
		carbs you are going to eat between 0g and 300g";
		document.getElementById("error").style.border = "10px solid red";
		return;
	}
	if(Cratio == NaN || Cratio < 1 || Cratio > 100)
	{
		document.getElementById("error").innerHTML = "Please enter how many carbs 1 unit of insulin covers";
		document.getElementById("error").style.border = "10px solid red";
		return;
	}
	if(correction == NaN ||correction < 10 || correction > 200)
	{
		document.getElementById("error").innerHTML = "Please enter the correction factor between 1 and 150 ";
		document.getElementById("error").style.border = "10px solid red";
		return;
	}
	if(tbg == NaN || tbg < 70 || tbg > 500) 
	{
		document.getElementById("error").innerHTML = "Please enter tbg bloodsugar in mg/DL, within the values of 70 and 500";
		document.getElementById("error").style.border = "10px solid red";
		return;
	}

	var CHO=(meal/Cratio);
	var HBS=((cbg-tbg)/correction);
	var TMID = (meal/Cratio) + ((cbg-tbg)/correction);

	document.getElementById("calculatedDoseBox3").innerHTML = "Carbohydrate Coverage Insulin Dose = " + CHO + " units of rapid acting insulin.";
	document.getElementById("calculatedDoseBox1").innerHTML = " Insulin Dose to Correct High Blood Sugar = " + HBS + " units of rapid acting insulin.";
	document.getElementById("calculatedDoseBox").innerHTML = "Total Mealtime Insulin Dose =" + TMID + " units of rapid acting insulin.";
	document.getElementById("calculatedDoseBox2").style.border = "10px solid black"
}

var meal = document.getElementById("n2")

