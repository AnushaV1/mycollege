    $('#funding-type').multiselect();
    const $results = $('#show_colleges');
    $("#search-form").on("submit", processForm);

    async function processForm(evt) {
        evt.preventDefault();
        const data = {
                "satOverall":parseInt($("#sat_score").val()),
                "zipCode":parseInt($("#zipcode").val()),
                "fundingType":$("#funding-type").val(),
        }
        if($("#max_tuition").val()){
            data.maxTuition = parseInt($("#max_tuition").val())
        }
        if($("#distance_from_home").val()) {
        data.distanceFromHomeMiles =[0,parseInt($("#distance_from_home").val())] 
        }
        if($('input[name="show_safeties"]').is(':checked')){
            data.show_safeties ="true"
            }
        if($('input[name="show_reaches"]').is(':checked')){
            data.show_reaches ="true"
        }
        if($('input[name="close_to_myscore"]').is(':checked')){
            data.closeToMyScores ="true"
        }
       
        let response = await axios.get("/api/get-college", {params: data});
        $("#search-form").trigger("reset");
        handleResponse(response)
    }
    /** handleResponse */
    
    function handleResponse(resp) {
        const data = resp['data']
        console.log(data)
        $results.empty();
        
        if(data =="false")
        {
            let noResultHTML = generateNoResultHTML();
                $results.append(noResultHTML);
        }
        
        else {
        for(let college of data) {
        const collegeMarkup = generateCollegeHTML(college);
        $results.append(collegeMarkup);
        }
        }
    }
    
    function generateNoResultHTML() {
    let noresult = `
    <div class="container">
    <div class="row">
    <div class="col-sm-12">
        <h1> NO RESULT FOUND... </h1>
    </div>
    </div>
    </div>`;
    return noresult;
    } 
    function generateCollegeHTML(college) {
        let description = college['shortDescription'] ?  college['shortDescription'] : '';
        let college_id = college['collegeUnitId']
            let collegeMarkup = `
            <div class="col-sm-4 col-mb-3">
            <div class="card">
            <div class="card-header bg-transparent border-success">  <img class="card-img-top" alt="${college['collegeId']}" src="${college['campusImage']}"/></div>
            <div class="card-body border-success"><h5 class="card-title">
            ${college['name']}</h5>
            <h5 class="card-subtitle mbr-fonts-style align-center display-4">${college['city']} ${college['stateAbbr']}</h5>
            <p class="card-text"><small class="text-muted"><a href="http://${college['website']}" class="card-link">${college['website']}</a></small></p>
            </div>
            <div class="card-footer bg-transparent">
            <form method="POST" class="shortlist-form">
            <input type="hidden" value="${college['name']}" data-id="${college['collegeUnitId']}">
            <button class="btn btn-md btn-custom pull-right">Shortlist</button>
            </form>
            <br>
            </div>
            <br>
            </div>
            <br>
        </div>`;
        
            return collegeMarkup;
    }
    
    $results.on('submit','.shortlist-form', async function(e){
        
        e.preventDefault();
        let shortlisted_data = {
                            "college_name":$(":hidden", this).val(),
                            "college_id":parseInt($(":hidden", this).data('id')),
                            }
        
        let response = await axios.get("/user/shortlist", {params: shortlisted_data});
        $(this).find('button').html('Shortlisted');
    
    })
    


