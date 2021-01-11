var lookup = {
    'AB':['Calgary', 'Edmonton', 'Red Deer'],
    'BC':['Victoria', 'Vancouver', 'Richmond', 'Burnaby', 'Kelowna'],
    'MB':['Winnipeg', 'Brandon', 'Steinbach'],
    'NB':['Fredericton', 'Saint John', 'Bathurst'],
    'NL':['St. John\'s', 'Labrador City'],
    'NS':['Halifax', 'Lunenburg', 'Truro', 'Dartmouth'],
    'ON':['Toronto', 'Ottawa', 'Hamilton', 'Windsor', 'London', 'Mississauga', 'Kingston', 'Markham'],
    'PE':['Charlottetown', 'Summerside'],
    'QC':['Montreal', 'Quebec City', 'Brossard', 'Laval', 'Trois-Rivères', 'Longueuil'],
    'SK':['Regina', 'Saskatoon'],
    'NT':['Yelloknife'],
    'NU':['Iqaluit'],
    'YT':['Whitehorse']
};

$('#inputProvinces').on('change', function(){

    var selectValue = $(this).val();

    for(i=0; i<lookup[selectValue].length; i++){
        for(j=0; j < (lookup[selectValue].length-1); j++){
            if (lookup[selectValue][j].charAt(1) > lookup[selectValue][j+1].charAt(1)){
                temp = lookup[selectValue][j];
                lookup[selectValue][j] = lookup[selectValue][j+1];
                lookup[selectValue][j+1] = temp;
            }
        }
    }

    for(i=0; i<lookup[selectValue].length; i++){
        for(j=0; j < (lookup[selectValue].length-1); j++){
            if (lookup[selectValue][j].charAt(0) > lookup[selectValue][j+1].charAt(0)){
                temp = lookup[selectValue][j];
                lookup[selectValue][j] = lookup[selectValue][j+1];
                lookup[selectValue][j+1] = temp;
            }
        }
    }



    $('#choices').empty();

    $('#choices').append("<option disabled selected>Select a city</option>")

    for(i=0; i< lookup[selectValue].length; i++){
        $('#choices').append("<option value=\'" + lookup[selectValue][i] + "\'>" + lookup[selectValue][i] + "</option>")
    }

    $('#choices').append("<option>Others</option>")

});