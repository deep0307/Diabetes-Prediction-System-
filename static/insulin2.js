const d=document.getElementById("calculatedDoseBox1");

const l=Math.log10;

const insulin=function()
{
	document.getElementById("error").style.border = null;
	document.getElementById("error").innerHTML = null;
	d.innerHTML='';

	const ins=document.getElementById("number1").value;
	const glu=document.getElementById("number2").value;

	const qi=1/(l(ins)+l(glu));


	if(qi>0.45)
		d.innerHTML="Congratulations: You are healthy!";
	else if(qi>0.3 && qi<=0.45)
		d.innerHTML="Hmmm: Possible resistence!";
	else
		d.innerHTML="😟️: Diabetic!";

	d.innerHTML+=`Quicki Index: ${qi}`;
}

