from fastapi import FastAPI
app = FastAPI()

@app.get("/even_odd/{n}")
def is_even(n : int):
    if(n % 2 == 0):
        result =  "even"
    else:
        result = "odd"
    
    return {
        "number" : n,
        "check_even" : n % 2 == 0,
        "msg" : f"{n} is {result}" 
    }
    

@app.get("/no")
def number():
    return {"msg" : "this is number"}
    
    