


const Header = () => {
    const webSiteName = 'AI Carbon Emission Measurement Tool';
    const logoUrl =
        'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MCA1MCI+PGRlZnM+PHN0eWxlPkBtZWRpYShtYXgtd2lkdGg6NDkuOThweCl7I2J7ZGlzcGxheTpub25lfX1AbWVkaWEobWluLXdpZHRoOjUwcHgpeyNje2Rpc3BsYXk6bm9uZX19PC9zdHlsZT48L2RlZnM+PHBhdGggZmlsbD0iI2ZmNzkwMCIgZD0iTTAgMGg1MHY1MEgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik03IDM1aDM1djdIN3oiIGlkPSJjIi8+PHBhdGggZmlsbD0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIuMTgiIGQ9Ik0xOS42MSA0NS4xNmE0LjEgNC4xIDAgMDEtMi4yOS42OWMtMS4zIDAtMi4wNi0uODctMi4wNi0yLjAyIDAtMS41NiAxLjQzLTIuMzkgNC4zOC0yLjcydi0uMzljMC0uNS0uMzktLjgtMS4xLS44YTIuMDcgMi4wNyAwIDAwLTEuNjkuOGwtMS4yMy0uN3EuOTctMS4zNiAyLjk2LTEuMzZjMS44MiAwIDIuODMuNzggMi44MyAyLjA2djUuMDVoLTEuNjN6bS0yLjU2LTEuNDdjMCAuNDcuMy45LjgyLjkuNTggMCAxLjE0LS4yMyAxLjctLjczdi0xLjY0Yy0xLjcxLjIxLTIuNTIuNjUtMi41MiAxLjQ4em01LjgtNC43bDEuNTEtLjIuMTcuODJjLjg2LS42MyAxLjU0LS45NiAyLjQtLjk2IDEuNDIgMCAyLjE2Ljc2IDIuMTYgMi4yN3Y0Ljg0aC0xLjgzdi00LjUyYzAtLjg2LS4yMi0xLjI0LS44OC0xLjI0LS41NSAwLTEuMS4yNS0xLjcxLjc3djVoLTEuODJ6bTE4LjM3IDYuOWMtMi4wNSAwLTMuMjctMS4zMS0zLjI3LTMuNiAwLTIuMyAxLjIzLTMuNjQgMy4yNC0zLjY0IDIuMDEgMCAzLjIgMS4yOCAzLjIgMy41NGwtLjAxLjM2aC00LjY0Yy4wMiAxLjMxLjU3IDEuOTggMS42NCAxLjk4LjcgMCAxLjE1LS4yOCAxLjU4LS44OGwxLjM0Ljc0Yy0uNTkuOTktMS42NSAxLjUtMy4wOCAxLjV6bTEuMzctNC41MmMwLS45My0uNTMtMS40OC0xLjQtMS40OC0uODIgMC0xLjM0LjUzLTEuNDEgMS40OHptLTM2LjQ0IDQuNmMtMS44IDAtMy40NC0xLjE1LTMuNDQtMy42N3MxLjYzLTMuNjcgMy40NC0zLjY3YzEuODIgMCAzLjQ1IDEuMTYgMy40NSAzLjY3IDAgMi41Mi0xLjY0IDMuNjctMy40NSAzLjY3em0wLTUuOGMtMS4zNiAwLTEuNjIgMS4yNC0xLjYyIDIuMTIgMCAuODguMjYgMi4xMyAxLjYyIDIuMTMgMS4zNyAwIDEuNjMtMS4yNCAxLjYzLTIuMTMgMC0uOS0uMjYtMi4xMi0xLjYzLTIuMTJ6bTQuNy0xLjM2aDEuNzR2LjgxYTIuNyAyLjcgMCAwMTEuOTItLjk2IDEuNTIgMS41MiAwIDAxLjI0LjAydjEuNzFoLS4wOWMtLjggMC0xLjY3LjEzLTEuOTQuNzV2NC42MmgtMS44N3ptMjIuNzIgNS40NmMxLjQgMCAxLjUxLTEuNDIgMS41MS0yLjM0IDAtMS4wOS0uNTMtMS45OC0xLjUyLTEuOTgtLjY2IDAtMS4zOS40OC0xLjM5IDIuMDUgMCAuODYuMDYgMi4yOCAxLjQgMi4yN3ptMy4yNy01LjQ4djYuNThjMCAxLjE3LS4wOSAzLjA4LTMuNCAzLjEtMS4zNyAwLTIuNjQtLjU0LTIuOS0xLjczbDEuODEtLjNjLjA4LjM1LjI5LjcgMS4zMS43Ljk1IDAgMS40MS0uNDYgMS40MS0xLjU1di0uODFsLS4wMi0uMDNjLS4zLjUyLS43MyAxLjAyLTEuOCAxLjAyLTEuNjIgMC0yLjktMS4xMy0yLjktMy40OCAwLTIuMzMgMS4zMi0zLjYzIDIuOC0zLjYzIDEuMzkgMCAxLjkuNjMgMi4wMi45NmgtLjAybC4xNS0uODN6bTguMjctMi4zMWgtLjcydjEuOTloLS4zOHYtMmgtLjcydi0uM2gxLjgyem0zIDEuOTloLS4zOHYtMS45MmgtLjAxbC0uNzUgMS45MmgtLjI0bC0uNzYtMS45MnYxLjkyaC0uMzl2LTIuM2guNTlsLjY4IDEuNzUuNjgtMS43NGguNTh6IiBpZD0iYiIvPjwvc3ZnPgo=';

    return (
        // <div className='header'>
        //     <div className='headerimg'>
        //        <img src={logoUrl} alt=""/>
        //     </div>
        //     <span className='headerwenzi'>
        //        {webSiteName}
        //     </span>
        // </div>
        <>
            <nav className="navbar navbar-dark bg-dark">
                <div className="container-fluid">
                    <div className="navbar-brand">
                        <span className="stretched-link">
                            <img src={logoUrl} width="50" height="50" alt="Boosted - Back to Home" loading="lazy"/>
                        </span>
                        <h2 className="title">{webSiteName}</h2>
                    </div>
                </div>
            </nav>
        </>
        
    );

}

export default Header;