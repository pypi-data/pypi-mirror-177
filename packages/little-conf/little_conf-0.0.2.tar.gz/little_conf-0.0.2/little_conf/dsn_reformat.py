class RedisDsn:
    @property
    def dsn(self) -> str:
        return RedisSettings._dsn_reformat(self.url, password=self.password or None)

    @staticmethod
    def _create_netloc(
        hostname: str,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> str:
        return '{cred}{host}{port}'.format(
            cred='{}:{}@'.format(username or '', password or '')
            if username is not None or password is not None
            else '',
            host=hostname,
            port=f':{port}' if port else '',
        )

    @staticmethod
    def _dsn_reformat(
        dsn: str, username: Optional[str] = None, password: Optional[str] = None
    ) -> str:
        o = urlsplit(dsn)
        new_netloc = RedisSettings._create_netloc(
            hostname=o.hostname or '',
            port=o.port,
            username=username if username is not None else o.username,
            password=password if password is not None else o.password,
        )
        return urlunsplit((o.scheme, new_netloc, o.path, o.query, o.fragment))


class PG:
    @property
    def dsn(self) -> str:
        url = make_url(self.url)
        # url = url.set(
        #     drivername='postgresql',
        #     username=self.username,
        #     password=self.password,
        # )
        if self.username:
            url = url.set(
                drivername='postgresql',
                username=self.username,
            )
        if self.password:
            url = url.set(
                drivername='postgresql',
                username=self.password,
            )
        return str(url)
