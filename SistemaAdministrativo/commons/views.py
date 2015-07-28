from django.shortcuts import render, redirect

def Error403(request, origen):
	return render(request, 'PermisoDenegado.html', {
			'origen': origen 
		})