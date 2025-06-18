import React from "react";
import { User } from "../../domain/types";

type Props = {
    children: React.ReactNode
}

const defaultUser = {
    user_id: 0,
    username: 'anonymous',
    email: 'anonymous@email.com',
    first_name: 'anonymous',
    last_name: 'anonymous'
}

export const UserContext = React.createContext<{ user: User, loading: boolean }>({ user: defaultUser, loading: false });

export const UserProvider: React.FC<Props> = ({ children }) => {
    const [user, setUser] = React.useState<User>(defaultUser)
    const [loading, setLoading] = React.useState(false)

    React.useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch('/api/users/me');
                const data = await response.json();
                setUser(data);
                setLoading(false);
            } catch (error) {
                console.error('Error al obtener los datos del usuario:', error);
            }
        };
        fetchUser();
        setLoading(true);
    }, []);



    return <UserContext.Provider value={{ user, loading }}>
        {children}
    </UserContext.Provider>
}
