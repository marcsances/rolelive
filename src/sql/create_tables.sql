CREATE TABLE Guild(
    guildId INT PRIMARY KEY,
    guildName TEXT
);

CREATE TABLE Role(
    guildId INT NOT NULL,
    roleId INT NOT NULL,
    adminRole BOOLEAN NOT NULL,
    roleName TEXT,
    PRIMARY KEY (guildId, roleId)
);

CREATE TABLE UserRoles(
    guildId INT NOT NULL,
    userId INT NOT NULL,
    roleId INT NOT NULL,
    FOREIGN KEY (guildId) REFERENCES Guild(guildId),
    FOREIGN KEY (guildId, roleId) REFERENCES Role(guildId, roleId),
    PRIMARY KEY (guildId, userId, roleId)
);

CREATE TABLE Stream(
    platformId INT NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    PRIMARY KEY (platformId, name)
);

CREATE TABLE StreamRecord(
    guildId INT NOT NULL,
    platformId INT NOT NULL,
    name TEXT NOT NULL,
    createdBy INT NOT NULL,
    FOREIGN KEY (guildId) REFERENCES Guild(guildId),
    FOREIGN KEY (platformId, name) REFERENCES Stream(platformId, name),
    PRIMARY KEY (guildId, platformId, name, createdBy)
);

CREATE TABLE GuildPreferences(
    guildId INT NOT NULL,
    prefKey TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (guildId) REFERENCES Guild(guildId),
    PRIMARY KEY (guildId, prefKey)
);

CREATE TABLE NotificationStyle(
    guildId INT NOT NULL,
    channelId INT NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY (guildId) REFERENCES Guild(guildId),
    PRIMARY KEY (guildId, channelId)
);

CREATE TABLE StreamFilters(
    guildId INT NOT NULL,
    filterId SERIAL,
    categoryMatch TEXT,
    titleMatch TEXT,
    FOREIGN KEY (guildId) REFERENCES Guild(guildId),
    PRIMARY KEY (guildId, filterId)
);

CREATE TABLE NotifiedChannels(
    guildId INT NOT NULL,
    filterId INT NOT NULL,
    channelId INT NOT NULL,
    FOREIGN KEY (guildId, filterId) REFERENCES StreamFilters(guildId, filterId),
    PRIMARY KEY (guildId, filterId, channelId)
);