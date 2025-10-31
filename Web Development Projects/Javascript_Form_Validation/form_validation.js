const form=document.querySelector("form")
const us=document.querySelector('#username')
const ps=document.querySelector("#password")
const em=document.querySelector("#email")
const bd=document.querySelector("#birthday")
const ad=document.querySelector("#address")
const ct=document.querySelector("#city")
const st=document.querySelector("#state")
const zp=document.querySelector("#zip")
const co=document.querySelector("#country")
const ph=document.querySelector("#phone")


const usererror=document.querySelector('#usererror')
const passerror=document.querySelector("#passerror")
const emailerror=document.querySelector("#emailerror")
const bderror=document.querySelector("#bderror")
const aderror=document.querySelector("#adderror")
const cityerror=document.querySelector("#cityerror")
const staterror=document.querySelector("#staterror")
const ziperror=document.querySelector("#ziperror")
const countryerror=document.querySelector("#countryerror")
const phonerror=document.querySelector("#phonerror")

function reseterrors() {
    usererror.textContent="";
    passerror.textContent="";
    emailerror.textContent="";
    bderror.textContent="";
    aderror.textContent="";
    cityerror.textContent="";
    ziperror.textContent="";
    countryerror.textContent="";
    phonerror.textContent="";
    staterror.textContent="";


    const l=[us,ps,em,bd,st,ct,zp,co,ph]
    l.forEach(a => a.classList.remove("error"));
}


form.addEventListener('submit',function(e) {
    e.preventDefault()
    let valid=true;
    reseterrors()
   

    if (us.value.trim()==='') {
        usererror.textContent="Username must be filled in";
        valid=false;
        us.classList.add("error")
    }

    if (co.value.trim()==='') {
        countryerror.textContent="Choose a country";
        valid=false;
        co.classList.add("error")
    }

    if (st.value.trim()==='') {
        staterror.textContent="Choose a state";
        valid=false;
        st.classList.add("error")
    }

    if (ad.value.trim()==="") {
        aderror.textContent="Enter an address";
        valid=false;
        ad.classList.add("error")

    }

     if (co.value.trim()==="") {
        countryerror.textContent="Enter an address";
        valid=false;
        co.classList.add("error")

    }
     if (ct.value.trim()==="") {
        cityerror.textContent="Enter an address";
        valid=false;
        ct.classList.add("error")

    }

    
    if (st.value.trim()==="") {
        staterror.textContent="Enter a state";
        valid=false;
        st.classList.add("error")

    }
    const zip_reg= /^\d{5}$/;
    if (zp.value.trim()==="") {
        ziperror.textContent="Enter a zip code";
        valid=false;
        zp.classList.add("error")

    }
    

    else if (!zip_reg.test(zp.value.trim())) {
       
       
        ziperror.textContent="Enter 5 digit zip code"
        valid=false;
        zp.classList.add("error")

    }

    


    const em_reg=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (em.value.trim()==='') {

        emailerror.textContent="Must enter an email address";
        valid=false;
        em.classList.add("error")
    }
        
    else if(!em_reg.test(em.value)){

        
        emailerror.textContent="Enter a valid email";
        valid=false;
        em.classList.add("error")
    }
    
    

    if (ps.value.trim() === "") {
        passerror.textContent="Enter a password";
        valid=false;
        ps.classList.add("error")
    }
    
    else if (ps.value.trim().length < 8) {
        
        passerror.textContent="Password must be 8 characters";
        valid=false;
        ps.classList.add("error")
    }
   
   

     const today = new Date();

        if(bd.value.trim()==="") {
        
        bderror.textContent="Select a date";
        valid=false;
        bd.classList.add("error")
    }
        else {
        const bd_date= new Date(bd.value);
        const date_valid=isNaN(bd_date.getTime());
       
        
        
        if (date_valid) {
        bderror.textContent="Select a valid date";
        valid=false;
        bd.classList.add("error")

        }
    
        else if (bd_date>today ) {
       
        bderror.textContent="Select a valid date";
        valid= false;
        bd.classList.add("error")
        }
    } 
    
        const phone_reg=/^\d{3}-\d{3}-\d{4}/;

        if (ph.value.trim()==="") {
             phonerror.textContent="Enter a zip code";
             valid=false;
            ph.classList.add("error")

    }
    

        else if (!phone_reg.test(zp.value.trim())) {
       
            phonerror.textContent="Enter a phone number: xxx-xxx-xxxx"
            valid=false;
            ph.classList.add("error")

    }



        if(valid) {
        alert("Form submitted successfully");
        form.submit();
    }
});
