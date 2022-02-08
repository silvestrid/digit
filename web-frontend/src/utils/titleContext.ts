import { createContext } from "react";

const TitleContext = createContext({
    title: "",
    setTitle: (title: string) => { }
});

export default TitleContext;