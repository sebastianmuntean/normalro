import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Avatar, Menu, MenuItem, IconButton, Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { AuthContext } from '../contexts/AuthContext';
import LanguageSelector from './LanguageSelector';
import Logo from './Logo';
import '../App.css'; // Import App.css for .App-header styles

const Navbar = () => {
  const { t } = useTranslation();
  const { user, setUser, setToken } = useContext(AuthContext);
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    handleClose();
    navigate('/login');
  };

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar 
      position="static" 
      className="App-header"
      sx={{ 
        backgroundColor: 'transparent',
        boxShadow: 'none',
        color: '#333'
      }}
    >
      <Toolbar>
        <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
          <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center' }}>
            <Logo color="#333" size={36} />
          </Link>
        </Box>
        {user && user.is_admin && (
          <Button sx={{ color: '#333' }} component={Link} to="/admin">{t('nav.admin')}</Button>
        )}
        <Box sx={{ mx: 1 }}>
          <LanguageSelector />
        </Box>
        {user ? (
          <Box>
            <IconButton onClick={handleMenu} sx={{ color: '#333' }} size="large">
              <Avatar sx={{ bgcolor: "#1976d2" }}>
                {user.username ? user.username[0].toUpperCase() : "U"}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
            >
              <Box sx={{ px: 2, py: 1 }}>
                <Typography variant="subtitle1">{user.username}</Typography>
                {user.email && (
                  <Typography variant="body2" color="text.secondary">{user.email}</Typography>
                )}
              </Box>
              <MenuItem onClick={() => { handleClose(); navigate('/profile'); }}>{t('nav.profile')}</MenuItem>
              <MenuItem onClick={handleLogout}>{t('nav.logout')}</MenuItem>
            </Menu>
          </Box>
        ) : (
          <Button sx={{ color: '#333' }} component={Link} to="/login">{t('nav.login')}</Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 