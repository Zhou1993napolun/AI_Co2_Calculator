import React from 'react';
import {Navigate, useRoutes} from 'react-router'

function MyRouter(props) {
    const router = useRoutes([
        {
            path: "/",
            element: <Navigate to="/indexPage"/>
        },
        {
            path: '/indexPage',
            element: lazyComponent("indexPage")
        },
    ])
    return (
        router
    );
}


const lazyComponent = (path) => {
    const Comp = React.lazy(() => import(`../views/${path}`))
    return (
        <React.Suspense fallback={<>Loading...</>}>
            <Comp/>
        </React.Suspense>
    )
}

export default MyRouter;
