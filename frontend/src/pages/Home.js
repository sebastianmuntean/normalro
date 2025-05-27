import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Container, Typography, Card, CardContent, TextField, Box, Pagination, MenuItem, Select, InputLabel, FormControl, Grid, Divider, Paper, IconButton, Collapse, InputAdornment } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import { formatHeaderDate, formatCompactDate } from '../services/dateService';
import API_BASE_URL from '../config/api';
import '../App.css'; // Import App.css for .App-header styles

const PAGE_SIZE = 10;

const Home = () => {
  const { t, i18n } = useTranslation();
  const [pages, setPages] = useState([]);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState('created_at_desc');
  const [searchOpen, setSearchOpen] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: PAGE_SIZE,
    total: 0,
    totalPages: 0,
    hasNext: false,
    hasPrev: false
  });
  const [loading, setLoading] = useState(false);

  const sortOptions = [
    { value: 'created_at_desc', label: t('home.sortBy.newest') },
    { value: 'created_at_asc', label: t('home.sortBy.oldest') },
    { value: 'title_asc', label: t('home.sortBy.titleAZ') },
    { value: 'title_desc', label: t('home.sortBy.titleZA') },
    { value: 'author_asc', label: t('home.sortBy.authorAZ') },
    { value: 'author_desc', label: t('home.sortBy.authorZA') },
  ];

  function extractFirstImage(html) {
    const match = html && html.match(/<img[^>]+src=["']([^"'>]+)["']/i);
    return match ? match[1] : null;
  }

  function extractExcerpt(html, maxLength = 120) {
    const text = html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
  }

  const fetchPages = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        limit: PAGE_SIZE,
        search,
        sort,
        status: 'published'
      };
      
      const response = await axios.get(API_BASE_URL + '/pages', { params });
      setPages(response.data.pages);
      setPagination(response.data.pagination);
    } catch (err) {
      console.error('Failed to load pages:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPages();
  }, [page, search, sort]);

  const handleSearchChange = e => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handleSortChange = e => {
    setSort(e.target.value);
    setPage(1);
  };

  const handlePageChange = (_, value) => {
    setPage(value);
  };

  const handleSearchToggle = () => {
    setSearchOpen(!searchOpen);
  };

  const handleSearchClose = () => {
    setSearchOpen(false);
    setSearch('');
    setPage(1);
  };

  const featuredArticle = pages[0];
  const otherArticles = pages.slice(1);

  return (
    <Box>
      {/* Header */}
      <div className="App-header">
        <Container>
          <div className="header-content">
            {/* Left side - Search */}
            <div className="search-section">
              <IconButton onClick={handleSearchToggle} size="small">
                <SearchIcon />
              </IconButton>
              <Collapse in={searchOpen} orientation="horizontal">
                <TextField 
                  placeholder={t('home.search')} 
                  value={search} 
                  onChange={handleSearchChange} 
                  size="small" 
                  sx={{ 
                    ml: 1, 
                    width: 250,
                    '& .MuiOutlinedInput-root': {
                      backgroundColor: '#f8f9fa'
                    }
                  }}
                  variant="outlined"
                  autoFocus={searchOpen}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={handleSearchClose} size="small">
                          <CloseIcon fontSize="small" />
                        </IconButton>
                      </InputAdornment>
                    )
                  }}
                />
              </Collapse>
            </div>

            {/* Right side - Sort */}
            <div className="sort-section">
              <FormControl size="small">
                <Select 
                  value={sort} 
                  onChange={handleSortChange} 
                  sx={{ minWidth: 120 }}
                  variant="outlined"
                  displayEmpty
                >
                  {sortOptions.map(opt => (
                    <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </div>
          </div>

          {/* Date */}
          <Typography variant="caption" className="date-text">
            {formatHeaderDate(new Date(), i18n.language)}
          </Typography>

          {/* Main Title */}
          <Typography variant="h3" className="main-title">
            {t('home.title')}
          </Typography>
        </Container>
      </div>

      <Container>
        {loading ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography>{t('home.loading')}</Typography>
          </Box>
        ) : (
          <>
            {/* Featured Article */}
            {featuredArticle && (
              <Box sx={{ mb: 4 }}>
                <Grid container spacing={3}>
                  <Grid size={{ xs: 12, md: 8 }}>
                    <Box>
                      <Typography variant="h4" sx={{ 
                        fontFamily: 'Georgia, serif', 
                        fontWeight: 'bold',
                        lineHeight: 1.2,
                        mb: 1
                      }}>
                        <Link 
                          to={"/page/" + featuredArticle.slug} 
                          style={{ 
                            textDecoration: 'none', 
                            color: 'inherit',
                            ':hover': { textDecoration: 'underline' }
                          }}
                        >
                          {featuredArticle.title}
                        </Link>
                      </Typography>
                      
                      <Typography variant="subtitle1" color="text.secondary" sx={{ 
                        fontFamily: 'Georgia, serif',
                        fontStyle: 'italic',
                        mb: 2,
                        lineHeight: 1.4
                      }}>
                        {extractExcerpt(featuredArticle.content, 200)}
                      </Typography>
                      
                      <Typography variant="caption" sx={{ 
                        fontWeight: 600,
                        textTransform: 'uppercase',
                        letterSpacing: 0.5
                      }}>
                        {t('home.by')} {featuredArticle.author} • {formatCompactDate(featuredArticle.created_at, i18n.language)}
                      </Typography>
                    </Box>
                  </Grid>
                  
                  <Grid size={{ xs: 12, md: 4 }}>
                    {extractFirstImage(featuredArticle.content) && (
                      <Box sx={{ 
                        width: '100%',
                        maxWidth: '300px',
                        aspectRatio: '1 / 1', // Modern CSS approach for square
                        position: 'relative',
                        overflow: 'hidden',
                        borderRadius: 1,
                        mx: 'auto', // Center the image
                        backgroundColor: '#f5f5f5' // Fallback background
                      }}>
                        <img 
                          src={extractFirstImage(featuredArticle.content)} 
                          alt="Featured" 
                          referrerPolicy="no-referrer"
                          style={{ 
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%', 
                            height: '100%', 
                            objectFit: 'cover',
                            objectPosition: 'center'
                          }}
                          onError={(e) => {
                            console.log('Image failed to load:', e.target.src);
                            // Hide the image container if it fails
                            e.target.style.display = 'none';
                          }}
                        />
                      </Box>
                    )}
                  </Grid>
                </Grid>
                
                <Divider sx={{ mt: 3, mb: 3 }} />
              </Box>
            )}

            {/* Other Articles Grid */}
            <Grid container spacing={3}>
              {otherArticles.map((article, index) => {
                const img = extractFirstImage(article.content);
                const excerpt = extractExcerpt(article.content, 100);
                
                return (
                  <Grid size={{ xs: 12, sm: 6, md: 4 }} key={article.id}>
                    <Box sx={{ 
                      height: '100%', 
                      display: 'flex', 
                      gap: 2,
                      alignItems: 'flex-start'
                    }}>
                      {/* Thumbnail on the left */}
                      {img && (
                        <Box sx={{ 
                          width: '120px',
                          height: '120px',
                          flexShrink: 0,
                          aspectRatio: '1 / 1',
                          position: 'relative',
                          overflow: 'hidden',
                          borderRadius: 1,
                          backgroundColor: '#f5f5f5' // Fallback background
                        }}>
                          <img 
                            src={img} 
                            alt="Article" 
                            referrerPolicy="no-referrer"
                            style={{ 
                              position: 'absolute',
                              top: 0,
                              left: 0,
                              width: '100%', 
                              height: '100%', 
                              objectFit: 'cover',
                              objectPosition: 'center'
                            }}
                            onError={(e) => {
                              console.log('Image failed to load:', e.target.src);
                              // Hide the image container if it fails
                              e.target.style.display = 'none';
                            }}
                          />
                        </Box>
                      )}
                      
                      {/* Text content on the right */}
                      <Box sx={{ flex: 1, minWidth: 0 }}>
                        <Typography variant="h6" sx={{ 
                          fontFamily: 'Georgia, serif',
                          fontWeight: 'bold',
                          lineHeight: 1.3,
                          mb: 1,
                          fontSize: '1.1rem'
                        }}>
                          <Link 
                            to={"/page/" + article.slug} 
                            style={{ 
                              textDecoration: 'none', 
                              color: 'inherit'
                            }}
                            onMouseEnter={(e) => e.target.style.textDecoration = 'underline'}
                            onMouseLeave={(e) => e.target.style.textDecoration = 'none'}
                          >
                            {article.title}
                          </Link>
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ 
                          mb: 1,
                          lineHeight: 1.4,
                          fontSize: '0.875rem'
                        }}>
                          {excerpt}
                        </Typography>
                        
                        <Typography variant="caption" sx={{ 
                          fontWeight: 600,
                          textTransform: 'uppercase',
                          letterSpacing: 0.5,
                          fontSize: '0.75rem'
                        }}>
                          {t('home.by')} {article.author} • {formatCompactDate(article.created_at, i18n.language)}
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                );
              })}
            </Grid>

            {/* Pagination */}
            {pagination.totalPages > 1 && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4, py: 3 }}>
                <Pagination 
                  count={pagination.totalPages} 
                  page={pagination.page} 
                  onChange={handlePageChange} 
                  color="primary"
                  size="large"
                />
              </Box>
            )}
          </>
        )}
      </Container>
    </Box>
  );
};

export default Home; 