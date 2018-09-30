let sorter = (function(console){ // eslint-disable-line no-unused-vars
    try {
        let LOG_ENUM = {
            "DEBUG": 2,
            "DEFAULT": 0
        };

        let LOG_LEVEL = LOG_ENUM["DEBUG"];

        let LOGGER;
        if (console && LOG_LEVEL > 0) {
            LOGGER = console;
        } else {
            LOGGER = {
                log: function() {},
                info: this.log,
                warn: this.log
            };
        }

        let setKey = (api_key) => {
            LOGGER.log("Setting api_key=" + api_key);
            localStorage.setItem("api_key", api_key);
        };

        let setUserId = (user_id) => {
            LOGGER.log("Setting user_id=" + user_id);
            localStorage.setItem("user_id", user_id);
        };

        let updateSettings = (form) => {
            const api_key = form.elements["api_key"].value;
            const user_id = form.elements["user_id"].value;

            setKey(api_key);
            setUserId(user_id);
            return false;
        };

        let serializeParams = (params) => {
            let queryString = "";
            for (let key in params) {
                if (params.hasOwnProperty(key)) {
                    let val = params[key];
                    queryString += `${key}=${val}&`;
                }
            }

            if (queryString.length) {
                queryString = "?" + queryString;
                queryString = queryString.slice(0, -1);
            }

            return queryString;
        };

        let importBooks = (myForm) => {
            let myPromise = new Promise((resolve, reject) => {
                let xhr = new XMLHttpRequest();
                let params = serializeParams({
                    api_key: myForm.elements["api_key"].value || "",
                    user_id: myForm.elements["user_id"].value || "",
                    new: 1,
                    per_page: myForm.elements["per_page"].value || "40"
                });
                xhr.open("POST", "http://localhost:8080/import", true);
                xhr.send(params);

                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200){
                            let response = xhr.responseText;
                            console.log(response);
                            let responseJson = JSON.parse(response);
                            resolve(responseJson);
                        } else {
                            reject(xhr.statusText);
                        }
                    }
                };
            });
            
            return myPromise;
        };

        let getKey = () => {
            return localStorage.getItem("api_key");
        };

        let getUserId = () => {
            return localStorage.getItem("user_id");
        };

        return {
            importBooks: importBooks,
            updateSettings: updateSettings,
            toggleEditable: function(el) {
                let parentEl = el.parentNode;
                let newEl = document.createElement("input");

                let column = document.getElementById(el.dataset.attr);
                let elName = column.textContent + "-" + el.dataset.book;

                newEl.value = el.textContent;
                newEl.name = elName;
                parentEl.insertBefore(newEl, el);

                el.style = "display:none;visibility:hidden";
            },
            init: (myForm) => {
                myForm.elements["api_key"].value = getKey();
                myForm.elements["user_id"].value = getUserId();
            }
        };
    } catch(e) {
        console.log(e);
    }
})(window.console);
